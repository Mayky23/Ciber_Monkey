$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$Status = [System.Collections.Generic.List[string]]::new()
$GoBin = Join-Path $HOME "go\bin"

function Add-Status {
    param([string]$Message)
    $Status.Add($Message) | Out-Null
}

function Say {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Cyan
}

function Warn {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Yellow
}

function Ensure-UserPath {
    param([string]$PathToAdd)
    $userPath = [Environment]::GetEnvironmentVariable("Path", "User")
    if (-not $userPath) {
        [Environment]::SetEnvironmentVariable("Path", $PathToAdd, "User")
        return
    }
    $parts = $userPath -split ';'
    if ($parts -notcontains $PathToAdd) {
        [Environment]::SetEnvironmentVariable("Path", ($userPath.TrimEnd(';') + ';' + $PathToAdd), "User")
    }
}

function Ensure-PythonLauncher {
    if (Get-Command py -ErrorAction SilentlyContinue) {
        return "py"
    }
    if (Get-Command python -ErrorAction SilentlyContinue) {
        return "python"
    }
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        Say "[*] Instalando Python..."
        winget install --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements --silent | Out-Null
        if (Get-Command py -ErrorAction SilentlyContinue) {
            return "py"
        }
        if (Get-Command python -ErrorAction SilentlyContinue) {
            return "python"
        }
    }
    throw "No se encontro Python en el sistema."
}

function Ensure-Go {
    if (Get-Command go -ErrorAction SilentlyContinue) {
        return
    }
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        Say "[*] Instalando Go..."
        winget install --id GoLang.Go --accept-package-agreements --accept-source-agreements --silent | Out-Null
    } elseif (Get-Command choco -ErrorAction SilentlyContinue) {
        Say "[*] Instalando Go..."
        choco install golang -y | Out-Null
    } else {
        throw "No se pudo instalar Go automaticamente."
    }
    if (-not (Get-Command go -ErrorAction SilentlyContinue)) {
        throw "Go no esta disponible tras la instalacion."
    }
}

function Install-GoTool {
    param(
        [string]$Label,
        [string]$Binary,
        [string]$Module
    )

    if (Get-Command $Binary -ErrorAction SilentlyContinue) {
        Add-Status("${Label}: OK")
        return
    }

    Ensure-Go
    & go install $Module | Out-Null
    Ensure-UserPath $GoBin
    $env:Path += ";$GoBin"

    if (Get-Command $Binary -ErrorAction SilentlyContinue) {
        Add-Status("${Label}: OK")
    } else {
        Add-Status("${Label}: instalado, abre una nueva terminal para usarlo")
    }
}

Say "[*] Preparando Ciber Monkey..."
$PythonLauncher = Ensure-PythonLauncher

Say "[*] Creando entorno virtual..."
if ($PythonLauncher -eq "py") {
    & py -3 -m venv .venv
} else {
    & python -m venv .venv
}

$VenvPython = ".\.venv\Scripts\python.exe"
Say "[*] Instalando dependencias Python..."
& $VenvPython -m pip install --upgrade pip setuptools wheel | Out-Null
& $VenvPython -m pip install -r requirements.txt | Out-Null
& $VenvPython -m pip install sqlmap | Out-Null
Add-Status("Python deps: OK")
Add-Status("sqlmap: OK (venv)")

if (-not (Get-Command nmap -ErrorAction SilentlyContinue)) {
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        Say "[*] Instalando Nmap..."
        winget install --id Insecure.Nmap --accept-package-agreements --accept-source-agreements --silent | Out-Null
    } elseif (Get-Command choco -ErrorAction SilentlyContinue) {
        Say "[*] Instalando Nmap..."
        choco install nmap -y | Out-Null
    }
}

if (Get-Command nmap -ErrorAction SilentlyContinue) {
    Add-Status("nmap: OK")
} else {
    Add-Status("nmap: pendiente")
}

if (Get-Command amass -ErrorAction SilentlyContinue) {
    Add-Status("amass: OK")
} else {
    Add-Status("amass: pendiente")
}

try {
    Install-GoTool -Label "subfinder" -Binary "subfinder" -Module "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"
    Install-GoTool -Label "gobuster" -Binary "gobuster" -Module "github.com/OJ/gobuster/v3@latest"
    Install-GoTool -Label "ffuf" -Binary "ffuf" -Module "github.com/ffuf/ffuf/v2@latest"
    Install-GoTool -Label "assetfinder" -Binary "assetfinder" -Module "github.com/tomnomnom/assetfinder@latest"
}
catch {
    Warn "[!] Algunas herramientas Go no pudieron instalarse automaticamente: $($_.Exception.Message)"
}

Write-Host ""
Write-Host "[+] Instalacion completada." -ForegroundColor Green
Write-Host "[+] Resumen:" -ForegroundColor Green
foreach ($line in $Status) {
    Write-Host "    - $line"
}
Write-Host "[+] Para ejecutar:" -ForegroundColor Green
Write-Host "    .\.venv\Scripts\Activate.ps1"
Write-Host "    python CiberMonkey.py"
