#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import getpass
import logging
import re
import sys
from dataclasses import dataclass
from typing import Iterable, Optional, Sequence, Dict, Any, List, Tuple

import pymysql
from pymysql.cursors import DictCursor
from Python.ui import draw_banner, pause


log = logging.getLogger("mysql_audit")

IDENT_RE = re.compile(r"^[A-Za-z0-9_]+$")
COMMON_ASCII = r"""
 DB Audit
"""
BANNER_COLOR = "\033[96m"


@dataclass
class Finding:
    schema: str
    table: str
    column: str
    data_type: str
    sample: Optional[str] = None
    count: Optional[int] = None


def safe_ident(name: str) -> str:
    """
    Very conservative identifier validation.
    Only allows letters, digits and underscore.
    """
    if not IDENT_RE.match(name):
        raise ValueError(f"Unsafe identifier: {name!r}")
    return f"`{name}`"


def mask_value(v: Any, keep: int = 3) -> str:
    if v is None:
        return "NULL"
    s = str(v)
    if len(s) <= keep * 2:
        return "*" * len(s)
    return f"{s[:keep]}***{s[-keep:]}"


def connect(host: str, user: str, password: str, port: int, db: Optional[str], ssl: bool) -> pymysql.connections.Connection:
    ssl_params = {"ssl": {}} if ssl else {}
    return pymysql.connect(
        host=host,
        user=user,
        password=password,
        port=port,
        database=db,
        cursorclass=DictCursor,
        read_timeout=15,
        write_timeout=15,
        connect_timeout=10,
        charset="utf8mb4",
        autocommit=True,
        **ssl_params,
    )


def fetch_one_value_dict(row: Dict[str, Any]) -> Any:
    # For statements like SHOW GRANTS where key name varies
    if not row:
        return None
    return next(iter(row.values()))


def check_user_permissions(conn: pymysql.connections.Connection) -> List[str]:
    grants: List[str] = []
    with conn.cursor() as cur:
        cur.execute("SHOW GRANTS FOR CURRENT_USER")
        for row in cur.fetchall():
            v = fetch_one_value_dict(row)
            if v is not None:
                grants.append(str(v))
    return grants


def analyze_security_configurations(conn: pymysql.connections.Connection) -> Dict[str, Any]:
    """
    Pull a small set of security-relevant knobs.
    Expand as needed for your baseline.
    """
    with conn.cursor() as cur:
        cur.execute("""
            SELECT
                @@version                  AS version,
                @@version_comment          AS version_comment,
                @@GLOBAL.sql_mode          AS global_sql_mode,
                @@SESSION.sql_mode         AS session_sql_mode,
                @@GLOBAL.local_infile      AS global_local_infile,
                @@GLOBAL.require_secure_transport AS require_secure_transport
        """)
        return cur.fetchone() or {}


def list_text_columns(conn: pymysql.connections.Connection, schema: str) -> List[Dict[str, Any]]:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = %s
              AND DATA_TYPE IN ('varchar','text','tinytext','mediumtext','longtext',
                                'char','tinyblob','blob','mediumblob','longblob')
            ORDER BY TABLE_NAME, ORDINAL_POSITION
            """,
            (schema,),
        )
        return cur.fetchall()


def find_sensitive_data(
    conn: pymysql.connections.Connection,
    schema: str,
    pattern: str,
    limit_tables: Optional[Sequence[str]] = None,
    max_rows_per_column: int = 3,
    count_only: bool = False,
) -> List[Finding]:
    """
    Searches pattern in text-like columns of the selected schema.

    - limit_tables: optional allowlist of table names
    - max_rows_per_column: sample rows per column
    - count_only: if True, returns only counts, no sample values
    """
    findings: List[Finding] = []
    cols = list_text_columns(conn, schema)

    allow_tables = set(limit_tables) if limit_tables else None

    for meta in cols:
        table = meta["TABLE_NAME"]
        column = meta["COLUMN_NAME"]
        data_type = meta["DATA_TYPE"]

        if allow_tables is not None and table not in allow_tables:
            continue

        # identifier safety
        t_ident = safe_ident(table)
        c_ident = safe_ident(column)

        with conn.cursor() as cur:
            if count_only:
                q = f"SELECT COUNT(*) AS cnt FROM {safe_ident(schema)}.{t_ident} WHERE {c_ident} LIKE %s"
                cur.execute(q, (f"%{pattern}%",))
                row = cur.fetchone() or {}
                cnt = int(row.get("cnt", 0))
                if cnt > 0:
                    findings.append(Finding(schema=schema, table=table, column=column, data_type=data_type, count=cnt))
            else:
                # Get a few samples (avoid SELECT *)
                q = (
                    f"SELECT {c_ident} AS val "
                    f"FROM {safe_ident(schema)}.{t_ident} "
                    f"WHERE {c_ident} LIKE %s "
                    f"LIMIT {int(max_rows_per_column)}"
                )
                cur.execute(q, (f"%{pattern}%",))
                rows = cur.fetchall()
                for r in rows:
                    findings.append(
                        Finding(
                            schema=schema,
                            table=table,
                            column=column,
                            data_type=data_type,
                            sample=mask_value(r.get("val")),
                        )
                    )

    return findings


def detect_plaintext_password_columns(conn: pymysql.connections.Connection, schema: str) -> List[Tuple[str, str, str]]:
    """
    Heurística: columnas con nombres típicos y tipo texto.
    No extrae valores.
    """
    name_markers = ("pass", "password", "pwd", "secret", "token", "apikey", "api_key")
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = %s
              AND DATA_TYPE IN ('varchar','text','tinytext','mediumtext','longtext','char')
            """,
            (schema,),
        )
        res = []
        for row in cur.fetchall():
            col = str(row["COLUMN_NAME"]).lower()
            if any(m in col for m in name_markers):
                res.append((row["TABLE_NAME"], row["COLUMN_NAME"], row["DATA_TYPE"]))
        return res


def print_section(title: str) -> None:
    print(f"\n[{title}]")


def print_audit_report(
    conn: pymysql.connections.Connection,
    schema: str,
    pattern: Optional[str] = None,
    limit_tables: Optional[Sequence[str]] = None,
    max_samples: int = 3,
    count_only: bool = False,
) -> None:
    grants = check_user_permissions(conn)
    cfg = analyze_security_configurations(conn)
    suspects = detect_plaintext_password_columns(conn, schema)

    print_section("Conexion")
    print("Conexion correcta con la base de datos.")

    print_section("Permisos")
    if grants:
        for grant in grants[:5]:
            print(f"- {grant}")
        if len(grants) > 5:
            print(f"- ... y {len(grants) - 5} permisos mas")
    else:
        print("- No se pudieron leer permisos.")

    print_section("Configuracion")
    print(f"- Version: {cfg.get('version', 'N/A')}")
    print(f"- Motor: {cfg.get('version_comment', 'N/A')}")
    print(f"- SQL Mode: {cfg.get('global_sql_mode', 'N/A')}")
    print(f"- local_infile: {cfg.get('global_local_infile', 'N/A')}")
    print(f"- secure_transport: {cfg.get('require_secure_transport', 'N/A')}")

    print_section("Columnas sensibles")
    if not suspects:
        print("- No se detectaron columnas sospechosas por nombre.")
    else:
        for table, column, data_type in suspects[:10]:
            print(f"- {table}.{column} ({data_type})")
        if len(suspects) > 10:
            print(f"- ... y {len(suspects) - 10} mas")

    if pattern:
        print_section("Busqueda por patron")
        print(f"- Patron usado: {pattern}")
        findings = find_sensitive_data(
            conn,
            schema=schema,
            pattern=pattern,
            limit_tables=limit_tables,
            max_rows_per_column=max_samples,
            count_only=count_only,
        )
        if not findings:
            print("- Sin coincidencias.")
        elif count_only:
            for finding in findings[:15]:
                print(f"- {finding.table}.{finding.column}: {finding.count} coincidencias")
            if len(findings) > 15:
                print(f"- ... y {len(findings) - 15} resultados mas")
        else:
            for finding in findings[:15]:
                print(f"- {finding.table}.{finding.column}: {finding.sample}")
            if len(findings) > 15:
                print(f"- ... y {len(findings) - 15} resultados mas")


def prompt_text(label: str, default: Optional[str] = None, secret: bool = False) -> Optional[str]:
    suffix = f" [{default}]" if default else ""
    raw = getpass.getpass(f"{label}{suffix}: ") if secret else input(f"{label}{suffix}: ")
    value = raw.strip()
    if value.lower() == "n":
        return None
    return value or default


def prompt_yes_no(label: str, default: bool = False) -> bool:
    default_label = "s" if default else "n"
    value = input(f"{label} (s/n) [{default_label}]: ").strip().lower()
    if not value:
        return default
    return value == "s"


def interactive_main() -> int:
    banner()
    print("Auditoria guiada para MySQL / MariaDB.")
    print("Escribe 'n' para volver en cualquier campo.\n")

    host = prompt_text("Host", "127.0.0.1")
    if host is None:
        return 0
    port_raw = prompt_text("Puerto", "3306")
    if port_raw is None:
        return 0
    user = prompt_text("Usuario")
    if user is None:
        return 0
    password = prompt_text("Password", secret=True)
    if password is None:
        return 0
    schema = prompt_text("Base de datos / schema")
    if schema is None or not schema:
        pause("Schema obligatorio. Pulsa Enter para volver...")
        return 1

    try:
        port = int(port_raw)
    except ValueError:
        pause("Puerto no valido. Pulsa Enter para volver...")
        return 1

    use_ssl = prompt_yes_no("Usar SSL/TLS", default=False)
    pattern = prompt_text("Patron opcional a buscar", "") or None
    count_only = prompt_yes_no("Mostrar solo conteos del patron", default=True) if pattern else False

    try:
        with connect(host, user, password, port, schema, use_ssl) as conn:
            banner()
            print_audit_report(
                conn,
                schema=schema,
                pattern=pattern,
                max_samples=3,
                count_only=count_only,
            )
            pause("\nPulsa Enter para volver...")
            return 0
    except (pymysql.Error, ValueError) as exc:
        pause(f"Error en la auditoria: {exc}\nPulsa Enter para volver...")
        return 1


def cli_main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="MySQL audit helper (lab/authorized use).")
    ap.add_argument("--host", required=True)
    ap.add_argument("--port", type=int, default=3306)
    ap.add_argument("--user", required=True)
    ap.add_argument("--password", required=True)
    ap.add_argument("--schema", required=True, help="Database/schema to audit")
    ap.add_argument("--ssl", action="store_true", help="Use TLS if supported")
    ap.add_argument("--pattern", default=None, help="Pattern to search in text columns (e.g. '@gmail.com', 'BEGIN RSA', 'IBAN')")
    ap.add_argument("--tables", nargs="*", default=None, help="Optional allowlist of tables to scan")
    ap.add_argument("--count-only", action="store_true", help="Only counts matches; no sample values")
    ap.add_argument("--max-samples", type=int, default=3, help="Max sample rows per column")
    ap.add_argument("-v", "--verbose", action="count", default=0)
    args = ap.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )

    try:
        with connect(args.host, args.user, args.password, args.port, args.schema, args.ssl) as conn:
            print_audit_report(
                conn,
                schema=args.schema,
                pattern=args.pattern,
                limit_tables=args.tables,
                max_samples=args.max_samples,
                count_only=args.count_only,
            )
            print("\nListo.")
            return 0

    except (pymysql.Error, ValueError) as e:
        log.error("Error: %s", e)
        return 1


def main() -> int:
    if len(sys.argv) > 1:
        return cli_main()
    return interactive_main()

def banner():
    draw_banner("", COMMON_ASCII, "MySQL / MariaDB", BANNER_COLOR)


if __name__ == "__main__":
    banner()
    raise SystemExit(main())
