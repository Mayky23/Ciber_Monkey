# Ciber Monkey

Ciber Monkey esta pensado para quien quiere lanzar una toolkit rapido sin ir buscando scripts sueltos por carpetas. Mezcla herramientas propias en Python con integraciones de binarios conocidos del ecosistema de ciberseguridad como `nmap`, `sqlmap`, `amass`, `assetfinder`, `gobuster` o `ffuf`.

![Menu principal](img/portada.png)

## Herramientas incluidas

Estas son las opciones actuales del menu principal:

- `DB Audit`: auditoria guiada de MySQL / MariaDB, con revision de grants, configuracion y columnas sensibles.
- `Calc CIDR`: calcula red, mascara, rango y datos utiles a partir de una IP/CIDR.
- `Data Gen`: genera datos ficticios para pruebas y desarrollo.
- `DDoS`: prueba controlada de disponibilidad/latencia sobre un servicio TCP autorizado.
- `File Guardian`: cifra y descifra archivos locales.
- `Port Listener`: abre un listener TCP sencillo para pruebas de conectividad.
- `Meta Spy`: lee metadatos y contenido basico de archivos.
- `Pwd Generator`: genera contrasenas personalizadas.
- `SQL Injection`: wrapper guiado para `sqlmap`.
- `Sub Finder`: enumeracion de subdominios usando herramientas externas.
- `Wifi Scanner`: descubrimiento LAN, puertos y redes WiFi.

## Requisitos

### Base

- Python 3.11 o superior
- `pip`
- `venv`

### Herramientas externas recomendadas

- `nmap`
- `sqlmap`
- `amass`
- `subfinder`
- `assetfinder`
- `gobuster`
- `ffuf`

### Librerias Python

Se instalan desde `requirements.txt`. Entre ellas:

- `requests`
- `cryptography`
- `pymysql`
- `dnspython`
- `exifread`
- `scapy`
- `pywifi`

## Instalacion rapida en Linux

La forma recomendada es usar el instalador incluido:

```bash
chmod +x install.sh
./install.sh
```

El instalador:

- instala los paquetes base necesarios
- crea el entorno virtual
- instala las dependencias Python
- intenta dejar `subfinder` disponible
- reintenta fuera del proyecto si la carpeta compartida no permite crear el `venv`

### Si el proyecto esta en una carpeta compartida

En Kali es comun que una carpeta montada o compartida falle al crear `.venv` por temas de enlaces simbolicos como `lib -> lib64`. El instalador ya contempla ese caso y puede mover el entorno a una ruta parecida a:

```bash
~/.virtualenvs/ciber_monkey
```

## Instalacion manual en Kali / Linux

Si prefieres hacerlo a mano:

```bash
sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-pip nmap sqlmap amass assetfinder gobuster ffuf libpcap-dev iputils-ping
python3 -m venv ~/.virtualenvs/ciber_monkey
source ~/.virtualenvs/ciber_monkey/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

Si luego quieres `subfinder` y no viene por paquete en tu sistema:

```bash
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```

## Instalacion en Windows

En PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\install.ps1
```

Si prefieres instalacion manual:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

## Como ejecutar la herramienta

### Kali / Linux

```bash
source ~/.virtualenvs/ciber_monkey/bin/activate
python CiberMonkey.py
```

Si el instalador te mostro otra ruta de entorno virtual, usa esa.

### Windows

```powershell
.\.venv\Scripts\Activate.ps1
python CiberMonkey.py
```

## Flujo recomendado de uso

1. Instala dependencias con `install.sh` o `install.ps1`.
2. Lanza `python CiberMonkey.py`.
3. Ejecuta la opcion `98` para revisar rapidamente el entorno.
4. Prueba primero las herramientas que no dependen de red externa.
5. Usa funciones ofensivas solo sobre objetivos autorizados.

## Dependencias por herramienta

- `DB Audit`: requiere acceso a una instancia MySQL/MariaDB.
- `Calc CIDR`: no depende de binarios externos.
- `Data Gen`: no depende de binarios externos.
- `DDoS`: no depende de binarios externos.
- `File Guardian`: depende de `cryptography`.
- `Port Listener`: no depende de binarios externos.
- `Meta Spy`: usa `exifread` para metadatos.
- `Pwd Generator`: no depende de binarios externos.
- `SQL Injection`: necesita `sqlmap`.
- `Sub Finder`: usa `amass`, `subfinder` y/o `assetfinder`.
- `Wifi Scanner`: usa `scapy`, `pywifi` y `nmap` segun disponibilidad.

## Notas importantes

- Algunas funciones de red pueden requerir privilegios elevados.
- `pywifi` puede no estar disponible o no comportarse igual en todos los entornos Linux.
- En laboratorios sin tarjeta WiFi compatible, el modulo de WiFi puede quedar parcialmente limitado.
- Si una herramienta externa no esta instalada, el diagnostico te lo indicara.

## Uso autorizado

Este proyecto esta pensado para:

- laboratorios
- maquinas propias
- entornos de pruebas
- auditorias con permiso expreso

No lo uses sobre sistemas, servicios o terceros sin autorizacion.

## Autor

- GitHub: [@Mayky23](https://github.com/Mayky23)
