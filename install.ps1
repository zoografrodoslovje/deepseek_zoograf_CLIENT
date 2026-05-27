<#
.SYNOPSIS
    DeepSeek Zoograf Client - Windows PowerShell Installer
.DESCRIPTION
    Sets up the HERO UI POR DeepSeek Agentic Terminal Client on Windows.
    Creates venv, installs deps, configures API key.
.NOTES
    Compatible with PowerShell 5.1+ and PowerShell 7+
#>

$Host.UI.RawUI.WindowTitle = "DeepSeek Zoograf Client - Setup"

# --- ANSI colors (PS 5.1 compatible: using [char]27) ---
$ESC = [char]27
$GREEN  = "${ESC}[92m"
$YELLOW = "${ESC}[93m"
$RED    = "${ESC}[91m"
$CYAN   = "${ESC}[96m"
$BOLD   = "${ESC}[1m"
$NC     = "${ESC}[0m"

Write-Host "${BOLD}===========================================${NC}"
Write-Host "${BOLD}   DeepSeek Zoograf Client - Setup        ${NC}"
Write-Host "${BOLD}   HERO UI POR - Agentic Terminal Client   ${NC}"
Write-Host "${BOLD}===========================================${NC}"
Write-Host ""

# --- Step 1: Check Python ---------------------------------
Write-Host "${CYAN}[1/5]${NC} Checking Python installation..."

try {
    $pyVersion = python --version 2>&1
} catch {
    Write-Host "${RED}[X] Python not found!${NC}"
    Write-Host ""
    Write-Host "  Download Python 3.10+ from:"
    Write-Host "${CYAN}https://www.python.org/downloads/${NC}"
    Write-Host ""
    Write-Host "  Make sure to check 'Add Python to PATH' during installation."
    Read-Host "Press Enter to exit"
    exit 1
}

if ($pyVersion -match "3\.(1[0-9]|[2-9]\d)\.") {
    Write-Host "${GREEN}[V]${NC} Python detected: $pyVersion"
} else {
    Write-Host "${YELLOW}[!] Warning: Python version may be below 3.10${NC}"
    Write-Host "  $pyVersion"
    $choice = Read-Host "  Continue anyway? (y/N)"
    if ($choice -ne "y" -and $choice -ne "Y") { exit 1 }
}

Write-Host ""

# --- Step 2: Create virtual environment --------------------
Write-Host "${CYAN}[2/5]${NC} Setting up virtual environment..."

if (Test-Path "venv") {
    Write-Host "${YELLOW}[!] Virtual environment already exists${NC}"
    $choice = Read-Host "  Recreate it? (y/N)"
    if ($choice -eq "y" -or $choice -eq "Y") {
        Remove-Item -Recurse -Force "venv"
        Write-Host "  Recreating..."
        python -m venv venv
    }
} else {
    python -m venv venv
}

if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "${RED}[X] Failed to create virtual environment${NC}"
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "${GREEN}[V]${NC} Virtual environment created"

# --- Step 3: Install dependencies --------------------------
Write-Host ""
Write-Host "${CYAN}[3/5]${NC} Installing Python dependencies..."
Write-Host "  This may take a minute..."

$pip = Join-Path (Get-Location) "venv\Scripts\pip.exe"
$null = & $pip install --upgrade pip 2>&1
$result = & $pip install -r requirements.txt 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "${RED}[X] Failed to install dependencies${NC}"
    Write-Host "  Error: $result"
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "${GREEN}[V]${NC} All dependencies installed"

# --- Step 4: Configure API key -----------------------------
Write-Host ""
Write-Host "${CYAN}[4/5]${NC} API Key configuration..."

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "${YELLOW}[!]${NC} Created .env from .env.example"
    Write-Host "  ${BOLD}IMPORTANT:${NC} You need to set your DeepSeek API key."
    Write-Host ""
    Write-Host "  1. Open ${BOLD}.env${NC} in a text editor"
    Write-Host "  2. Replace ${YELLOW}sk-your-key-here${NC} with your actual API key"
    Write-Host "  3. Save the file"
    Write-Host ""
    Write-Host "  Get a key at: ${CYAN}https://platform.deepseek.com/api_keys${NC}"
    Write-Host ""
    & notepad .env
} else {
    Write-Host "${GREEN}[V]${NC} .env already exists"
}

# --- Step 5: Verify installation ---------------------------
Write-Host ""
Write-Host "${CYAN}[5/5]${NC} Verifying installation..."

$python = Join-Path (Get-Location) "venv\Scripts\python.exe"
$result = & $python -c "import textual; import openai; import rich; print('[V] All imports OK')" 2>&1
Write-Host "  $result"

Write-Host ""
Write-Host "${GREEN}${BOLD}===========================================${NC}"
Write-Host "${GREEN}${BOLD}  Setup Complete!                          ${NC}"
Write-Host "${GREEN}${BOLD}-------------------------------------------${NC}"
Write-Host "${GREEN}${BOLD}                                          ${NC}"
Write-Host "${GREEN}${BOLD}  Run the client:                         ${NC}"
Write-Host "${GREEN}${BOLD}     .\run.bat                              ${NC}"
Write-Host "${GREEN}${BOLD}     or                                     ${NC}"
Write-Host "${GREEN}${BOLD}     venv\Scripts\activate ; python main.py  ${NC}"
Write-Host "${GREEN}${BOLD}                                          ${NC}"
Write-Host "${GREEN}${BOLD}===========================================${NC}"
Write-Host ""

Read-Host "Press Enter to exit"
