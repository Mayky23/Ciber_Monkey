$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "[*] Creando entorno virtual..." -ForegroundColor Cyan
py -3 -m venv .venv

Write-Host "[*] Activando entorno e instalando dependencias..." -ForegroundColor Cyan
& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip setuptools wheel
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt

if (-not (Get-Command nmap -ErrorAction SilentlyContinue)) {
    Write-Host "[!] Nmap no esta en PATH. Algunas funciones de escaneo avanzado no estaran disponibles hasta instalarlo." -ForegroundColor Yellow
}

if (-not (Get-Command sqlmap -ErrorAction SilentlyContinue)) {
    Write-Host "[!] sqlmap no esta en PATH. La opcion de revision SQLi no estara disponible hasta instalarlo." -ForegroundColor Yellow
}

if (
    -not (Get-Command amass -ErrorAction SilentlyContinue) -and
    -not (Get-Command subfinder -ErrorAction SilentlyContinue) -and
    -not (Get-Command assetfinder -ErrorAction SilentlyContinue)
) {
    Write-Host "[!] No hay herramientas de subdominios en PATH. Instala amass, subfinder o assetfinder si quieres esa opcion." -ForegroundColor Yellow
}

if (
    -not (Get-Command gobuster -ErrorAction SilentlyContinue) -and
    -not (Get-Command ffuf -ErrorAction SilentlyContinue)
) {
    Write-Host "[!] No hay herramientas de directorios web en PATH. Instala gobuster o ffuf si quieres esa opcion." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[+] Instalacion terminada." -ForegroundColor Green
Write-Host "[+] Para ejecutar:" -ForegroundColor Green
Write-Host "    .\.venv\Scripts\Activate.ps1"
Write-Host "    python CiberMonkey.py"
