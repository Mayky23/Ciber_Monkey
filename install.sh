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
APT_PACKAGES=(
  python3
  python3-venv
  python3-pip
  nmap
  sqlmap
  amass
  assetfinder
  gobuster
  ffuf
  libpcap-dev
  iputils-ping
)

say() {
  printf '%s\n' "$1"
}

create_venv() {
  local target="$1"
  rm -rf "$target"
  mkdir -p "$(dirname "$target")"
  python3 -m venv "$target"
  [[ -x "$target/bin/python" || -x "$target/bin/python3" ]]
}

install_subfinder() {
  if command -v subfinder >/dev/null 2>&1; then
    return 0
  fi

  if command -v apt-cache >/dev/null 2>&1 && apt-cache show subfinder >/dev/null 2>&1; then
    sudo apt-get install -y -qq subfinder >/dev/null 2>&1 || true
  fi

  if command -v subfinder >/dev/null 2>&1; then
    return 0
  fi

  if ! command -v go >/dev/null 2>&1; then
    sudo apt-get install -y -qq golang-go >/dev/null 2>&1 || return 1
  fi

  GO111MODULE=on go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest >/dev/null 2>&1 || return 1
  export PATH="$PATH:$REAL_HOME/go/bin"

  if [[ -d "$REAL_HOME/go/bin" ]] && ! grep -qs 'go/bin' "$REAL_HOME/.bashrc" 2>/dev/null; then
    printf '\nexport PATH="$PATH:%s/go/bin"\n' "$REAL_HOME" >> "$REAL_HOME/.bashrc"
  fi

  command -v subfinder >/dev/null 2>&1
}

say "[*] Preparando Ciber Monkey..."

if command -v apt-get >/dev/null 2>&1; then
  say "[*] Instalando paquetes base..."
  sudo apt-get update -qq >/dev/null
  sudo apt-get install -y -qq "${APT_PACKAGES[@]}" >/dev/null
else
  say "[!] No se detecto apt-get. Instala manualmente Python 3, venv, nmap, sqlmap y las herramientas externas."
fi

say "[*] Creando entorno Python..."
if create_venv "$VENV_DIR" >/dev/null 2>&1; then
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

say "[*] Comprobando herramientas adicionales..."
if install_subfinder; then
  SUBFINDER_STATUS="OK"
else
  SUBFINDER_STATUS="Pendiente"
fi

say ""
say "[+] Instalacion completada."
say "[+] Entorno virtual: $ACTIVE_VENV"
say "[+] Estado subfinder: $SUBFINDER_STATUS"
say "[+] Para abrir la herramienta:"
say "    source \"$ACTIVE_VENV/bin/activate\""
say "    python CiberMonkey.py"
