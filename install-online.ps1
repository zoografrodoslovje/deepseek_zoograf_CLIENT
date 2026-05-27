<#
.SYNOPSIS
    DeepSeek Zoograf Client - One-Shot Online Installer
.DESCRIPTION
    Downloads and installs the HERO UI POR DeepSeek Agentic Terminal Client.
    Run this from PowerShell with:
        iex (iwr -UseBasicParsing -Uri https://raw.githubusercontent.com/zoografrodoslovje/deepseek_zoograf_CLIENT/main/install-online.ps1)
.NOTES
    Requires: Windows 10+, PowerShell 5.1+, Python 3.10+
#>

$Host.UI.RawUI.WindowTitle = "DeepSeek Zoograf Client - One-Shot Install"

# --- ANSI colors (PS 5.1 compatible: [char]27 instead of `e) ---
$ESC = [char]27
$GREEN  = "${ESC}[92m"
$YELLOW = "${ESC}[93m"
$RED    = "${ESC}[91m"
$CYAN   = "${ESC}[96m"
$BOLD   = "${ESC}[1m"
$NC     = "${ESC}[0m"

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
    Write-Host "  Directory exists. Updating..."
    Push-Location $destDir
    # Capture stderr from git into a string so it doesn't trigger errors
    $gitErr = $null
    $null = & git pull 2>&1
    Pop-Location
} else {
    if (Get-Command git -ErrorAction SilentlyContinue) {
        Write-Host "  Cloning with git..."
        $null = & git clone $repoUrl 2>&1
    } else {
        Write-Host "  Git not found, downloading ZIP..."
        $zipUrl = "$repoUrl/archive/refs/heads/main.zip"
        $zipPath = Join-Path $env:TEMP "ds-zoograf.zip"
        Remove-Item $zipPath -ErrorAction SilentlyContinue
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12
        $webClient = New-Object System.Net.WebClient
        $webClient.DownloadFile($zipUrl, $zipPath)
        Expand-Archive $zipPath -DestinationPath (Get-Location) -Force
        $extracted = Join-Path (Get-Location) "deepseek_zoograf_CLIENT-main"
        if (Test-Path $extracted) {
            Remove-Item $destDir -Recurse -Force -ErrorAction SilentlyContinue
            Rename-Item $extracted $destDir
        }
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
    Write-Host "  Removing old virtual environment..."
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
$null = & $pip install --upgrade pip 2>&1
$result = & $pip install -r requirements.txt 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "${RED}[X] Failed to install dependencies${NC}"
    Write-Host "  Error: $result"
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
    & notepad .env
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
Write-Host "${GREEN}${BOLD}  Or manually:                             ${NC}"
Write-Host "${GREEN}${BOLD}     venv\Scripts\activate                  ${NC}"
Write-Host "${GREEN}${BOLD}     python main.py                        ${NC}"
Write-Host "${GREEN}${BOLD}                                          ${NC}"
Write-Host "${GREEN}${BOLD}===========================================${NC}"
Write-Host ""

Pop-Location
Read-Host "Press Enter to exit"
