#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

resolve_real_home() {
  if [[ -n "${SUDO_USER:-}" && "${SUDO_USER}" != "root" ]]; then
    getent passwd "$SUDO_USER" | cut -d: -f6
    return
  fi
  if [[ -n "${HOME:-}" ]]; then
    printf '%s\n' "$HOME"
    return
  fi
  getent passwd "$(id -un)" | cut -d: -f6
}

REAL_HOME="$(resolve_real_home)"
VENV_DIR="${VENV_DIR:-$ROOT_DIR/.venv}"
FALLBACK_VENV_DIR="${FALLBACK_VENV_DIR:-$REAL_HOME/.virtualenvs/ciber_monkey}"
PKG_MANAGER=""
GO_BIN_DIR="$REAL_HOME/go/bin"
INSTALL_STATUS=()

say() {
  printf '%s\n' "$1"
}

warn() {
  printf '%s\n' "$1"
}

record_status() {
  INSTALL_STATUS+=("$1")
}

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

create_venv() {
  local target="$1"
  rm -rf "$target"
  mkdir -p "$(dirname "$target")"
  "${PYTHON_BIN:-python3}" -m venv "$target"
  [[ -x "$target/bin/python" || -x "$target/bin/python3" ]]
}

detect_package_manager() {
  if command_exists apt-get; then
    PKG_MANAGER="apt"
  elif command_exists dnf; then
    PKG_MANAGER="dnf"
  elif command_exists pacman; then
    PKG_MANAGER="pacman"
  elif command_exists zypper; then
    PKG_MANAGER="zypper"
  elif command_exists apk; then
    PKG_MANAGER="apk"
  else
    PKG_MANAGER=""
  fi
}

package_exists() {
  local package="$1"
  case "$PKG_MANAGER" in
    apt) apt-cache show "$package" >/dev/null 2>&1 ;;
    dnf) dnf info "$package" >/dev/null 2>&1 ;;
    pacman) pacman -Si "$package" >/dev/null 2>&1 ;;
    zypper) zypper --non-interactive info "$package" >/dev/null 2>&1 ;;
    apk) apk search -e "$package" >/dev/null 2>&1 ;;
    *) return 1 ;;
  esac
}

install_packages() {
  local packages=("$@")
  [[ ${#packages[@]} -eq 0 ]] && return 0
  case "$PKG_MANAGER" in
    apt) sudo apt-get install -y -qq "${packages[@]}" >/dev/null ;;
    dnf) sudo dnf install -y -q "${packages[@]}" >/dev/null ;;
    pacman) sudo pacman -S --noconfirm --needed "${packages[@]}" >/dev/null ;;
    zypper) sudo zypper --non-interactive install --no-recommends "${packages[@]}" >/dev/null ;;
    apk) sudo apk add --no-progress "${packages[@]}" >/dev/null ;;
    *) return 1 ;;
  esac
}

install_first_available() {
  local label="$1"
  shift
  local candidate
  for candidate in "$@"; do
    if package_exists "$candidate"; then
      install_packages "$candidate"
      record_status "$label: OK ($candidate)"
      return 0
    fi
  done
  record_status "$label: no disponible en repositorio"
  return 1
}

ensure_path_line() {
  local shell_rc="$1"
  local path_line="$2"
  touch "$shell_rc"
  grep -qsF "$path_line" "$shell_rc" || printf '\n%s\n' "$path_line" >> "$shell_rc"
}

ensure_go() {
  if command_exists go; then
    return 0
  fi

  install_first_available "Go" golang-go golang go >/dev/null 2>&1 || return 1
  command_exists go
}

install_go_tool() {
  local label="$1"
  local binary="$2"
  local module="$3"

  if command_exists "$binary" || [[ -x "$GO_BIN_DIR/$binary" ]]; then
    record_status "$label: OK"
    return 0
  fi

  ensure_go || {
    record_status "$label: fallo instalando Go"
    return 1
  }

  GO111MODULE=on go install "$module" >/dev/null 2>&1 || {
    record_status "$label: fallo instalacion"
    return 1
  }

  export PATH="$PATH:$GO_BIN_DIR"
  ensure_path_line "$REAL_HOME/.bashrc" "export PATH=\"\$PATH:$GO_BIN_DIR\""
  ensure_path_line "$REAL_HOME/.zshrc" "export PATH=\"\$PATH:$GO_BIN_DIR\""

  if command_exists "$binary" || [[ -x "$GO_BIN_DIR/$binary" ]]; then
    record_status "$label: OK"
    return 0
  fi

  record_status "$label: instalado pero no visible en PATH actual"
  return 1
}

install_sqlmap() {
  local pkg_status=1

  if command_exists sqlmap; then
    record_status "sqlmap: OK"
    return 0
  fi

  if install_first_available "sqlmap" sqlmap >/dev/null 2>&1; then
    pkg_status=0
  fi

  if command_exists sqlmap; then
    return 0
  fi

  python -m pip install sqlmap >/dev/null 2>&1 || {
    if [[ $pkg_status -ne 0 ]]; then
      record_status "sqlmap: fallo instalacion"
    fi
    return 1
  }
  record_status "sqlmap: OK (pip)"
}

say "[*] Preparando Ciber Monkey..."

detect_package_manager

if [[ -n "$PKG_MANAGER" ]]; then
  say "[*] Detectado gestor: $PKG_MANAGER"
  say "[*] Instalando base del sistema..."
  case "$PKG_MANAGER" in
    apt) sudo apt-get update -qq >/dev/null ;;
    dnf) sudo dnf makecache -q >/dev/null ;;
    pacman) sudo pacman -Sy --noconfirm >/dev/null ;;
    zypper) sudo zypper --non-interactive refresh >/dev/null ;;
    apk) sudo apk update >/dev/null ;;
  esac

  install_first_available "Python" python3 python >/dev/null 2>&1 || true
  install_first_available "pip" python3-pip py3-pip python-pip >/dev/null 2>&1 || true
  install_first_available "venv" python3-venv python-virtualenv py3-virtualenv >/dev/null 2>&1 || true
  install_first_available "Git" git >/dev/null 2>&1 || true
  install_first_available "curl" curl >/dev/null 2>&1 || true
  install_first_available "certificados" ca-certificates ca-certificates-utils >/dev/null 2>&1 || true
  install_first_available "libpcap" libpcap-dev libpcap-devel libpcap >/dev/null 2>&1 || true
  install_first_available "ping" iputils-ping iputils busybox-extras >/dev/null 2>&1 || true
  install_first_available "wpa_supplicant" wpa_supplicant >/dev/null 2>&1 || true
  install_first_available "nmap" nmap >/dev/null 2>&1 || true
  install_first_available "amass" amass >/dev/null 2>&1 || true
else
  warn "[!] No se detecto un gestor compatible. Continuare con instalacion Python y fallbacks."
fi

if ! command_exists python3 && ! command_exists python; then
  warn "[!] No se encontro Python. Instala Python 3 y vuelve a ejecutar el script."
  exit 1
fi

PYTHON_BIN="$(command -v python3 || command -v python)"

say "[*] Creando entorno Python..."
if PYTHON_BIN="$PYTHON_BIN" create_venv "$VENV_DIR" >/dev/null 2>&1; then
  ACTIVE_VENV="$VENV_DIR"
else
  say "[*] La carpeta actual no permite crear el entorno. Usare esta ruta:"
  say "    $FALLBACK_VENV_DIR"
  create_venv "$FALLBACK_VENV_DIR"
  ACTIVE_VENV="$FALLBACK_VENV_DIR"
fi

say "[*] Instalando dependencias Python..."
source "$ACTIVE_VENV/bin/activate"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install -r requirements.txt >/dev/null
record_status "Python deps: OK"

say "[*] Instalando herramientas adicionales..."
install_sqlmap || true
install_go_tool "subfinder" "subfinder" "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest" || true
install_go_tool "gobuster" "gobuster" "github.com/OJ/gobuster/v3@latest" || true
install_go_tool "ffuf" "ffuf" "github.com/ffuf/ffuf/v2@latest" || true
install_go_tool "assetfinder" "assetfinder" "github.com/tomnomnom/assetfinder@latest" || true

say ""
say "[+] Instalacion completada."
say "[+] Entorno virtual: $ACTIVE_VENV"
say "[+] Resumen:"
for line in "${INSTALL_STATUS[@]}"; do
  say "    - $line"
done
say "[+] Para abrir la herramienta:"
say "    source \"$ACTIVE_VENV/bin/activate\""
say "    python CiberMonkey.py"
