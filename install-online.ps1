<#
.SYNOPSIS
    DeepSeek Zoograf Client - One-Shot Online Installer
.DESCRIPTION
    Downloads and installs the HERO UI POR DeepSeek Agentic Terminal Client.
    Run this from PowerShell with:
        iex (iwr -Uri https://raw.githubusercontent.com/zoografrodoslovje/deepseek_zoograf_CLIENT/main/install-online.ps1)
.NOTES
    Requires: Windows 10+, PowerShell 5.1+, Python 3.10+
#>

$Host.UI.RawUI.WindowTitle = "DeepSeek Zoograf Client - One-Shot Install"
$ErrorActionPreference = "Stop"

$GREEN  = "`e[92m"
$YELLOW = "`e[93m"
$RED    = "`e[91m"
$CYAN   = "`e[96m"
$BOLD   = "`e[1m"
$NC     = "`e[0m"

Write-Host "${BOLD}===========================================${NC}"
Write-Host "${BOLD}   DeepSeek Zoograf Client                 ${NC}"
Write-Host "${BOLD}   One-Shot Online Installer                ${NC}"
Write-Host "${BOLD}===========================================${NC}"
Write-Host ""

# --- Step 1: Check Python --------------------
Write-Host "${CYAN}[1/4]${NC} Checking prerequisites..."

try {
    $pyVersion = python --version 2>&1
} catch {
    Write-Host "${RED}[X] Python not found!${NC}"
    Write-Host "  Download Python 3.10+ from:"
    Write-Host "${CYAN}https://www.python.org/downloads/${NC}"
    Read-Host "Press Enter to exit"
    exit 1
}

if ($pyVersion -match "3\.(1[0-9]|[2-9]\d)\.") {
    Write-Host "${GREEN}[V]${NC} $pyVersion"
} else {
    Write-Host "${YELLOW}[!] Python may be below 3.10: $pyVersion${NC}"
    $choice = Read-Host "  Continue anyway? (y/N)"
    if ($choice -ne "y" -and $choice -ne "Y") { exit 1 }
}

# --- Step 2: Download repo --------------------
Write-Host ""
Write-Host "${CYAN}[2/4]${NC} Downloading DeepSeek Zoograf Client..."

$repoUrl = "https://github.com/zoografrodoslovje/deepseek_zoograf_CLIENT"
$destDir = Join-Path (Get-Location) "deepseek_zoograf_CLIENT"

if (Test-Path $destDir) {
    Write-Host "  Directory exists. Pulling latest..."
    Push-Location $destDir
    & git pull 2>&1 | Out-Null
    Pop-Location
} else {
    # Try git first, fall back to ZIP download
    if (Get-Command git -ErrorAction SilentlyContinue) {
        Write-Host "  Cloning with git..."
        & git clone $repoUrl 2>&1
    } else {
        Write-Host "  Downloading ZIP (git not found)..."
        $zipUrl = "$repoUrl/archive/refs/heads/main.zip"
        $zipPath = Join-Path $env:TEMP "ds-zoograf.zip"
        Remove-Item $zipPath -ErrorAction SilentlyContinue
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12
        $webClient = New-Object System.Net.WebClient
        $webClient.DownloadFile($zipUrl, $zipPath)
        Expand-Archive $zipPath -DestinationPath (Get-Location) -Force
        Rename-Item (Join-Path (Get-Location) "deepseek_zoograf_CLIENT-main") $destDir -ErrorAction SilentlyContinue
    }
}

if (-not (Test-Path $destDir)) {
    Write-Host "${RED}[X] Failed to download the client${NC}"
    Read-Host "Press Enter to exit"
    exit 1
}

Push-Location $destDir
Write-Host "${GREEN}[V]${NC} Downloaded to: $destDir"

# --- Step 3: Install dependencies ------------
Write-Host ""
Write-Host "${CYAN}[3/4]${NC} Setting up Python virtual environment..."

if (Test-Path "venv") {
    Write-Host "  Virtual environment already exists, recreating..."
    Remove-Item -Recurse -Force "venv"
}
python -m venv venv

if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "${RED}[X] Failed to create virtual environment${NC}"
    Pop-Location
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "${GREEN}[V]${NC} Virtual environment created"

Write-Host ""
Write-Host "  Installing dependencies..."
$pip = Join-Path (Get-Location) "venv\Scripts\pip.exe"
& $pip install --upgrade pip | Out-Null
& $pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "${RED}[X] Failed to install dependencies${NC}"
    Pop-Location
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "${GREEN}[V]${NC} All dependencies installed"

# --- Step 4: Configure API key ---------------
Write-Host ""
Write-Host "${CYAN}[4/4]${NC} API Key configuration..."

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "${YELLOW}[!]${NC} Created .env file."
    Write-Host "  ${BOLD}IMPORTANT:${NC} You must add your DeepSeek API key."
    Write-Host ""
    Write-Host "  1. Open .env in a text editor"
    Write-Host "  2. Replace 'sk-your-key-here' with your API key"
    Write-Host "  3. Save the file"
    Write-Host ""
    Write-Host "  Get a free key: ${CYAN}https://platform.deepseek.com/api_keys${NC}"
    Write-Host ""
    notepad .env
} else {
    Write-Host "${GREEN}[V]${NC} .env already configured"
}

# --- Done ---
Write-Host ""
Write-Host "${GREEN}${BOLD}===========================================${NC}"
Write-Host "${GREEN}${BOLD}  Installation Complete!                   ${NC}"
Write-Host "${GREEN}${BOLD}-------------------------------------------${NC}"
Write-Host "${GREEN}${BOLD}                                          ${NC}"
Write-Host "${GREEN}${BOLD}  To launch the client:                   ${NC}"
Write-Host "${GREEN}${BOLD}                                          ${NC}"
Write-Host "${GREEN}${BOLD}     cd deepseek_zoograf_CLIENT            ${NC}"
Write-Host "${GREEN}${BOLD}     .\run.bat                              ${NC}"
Write-Host "${GREEN}${BOLD}                                          ${NC}"
Write-Host "${GREEN}${BOLD}  Or activate first, then run:            ${NC}"
Write-Host "${GREEN}${BOLD}     venv\Scripts\activate                 ${NC}"
Write-Host "${GREEN}${BOLD}     python main.py                        ${NC}"
Write-Host "${GREEN}${BOLD}                                          ${NC}"
Write-Host "${GREEN}${BOLD}===========================================${NC}"
Write-Host ""

Pop-Location
Read-Host "Press Enter to exit"
