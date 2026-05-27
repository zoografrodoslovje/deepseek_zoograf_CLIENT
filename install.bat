@echo off
title DeepSeek Zoograf Client — Setup
chcp 65001 >nul

:: ─────────────────────────────────────────────
:: DeepSeek Zoograf Client — Windows Installer
:: ─────────────────────────────────────────────

setlocal enabledelayedexpansion

set "GREEN=[92m"
set "YELLOW=[93m"
set "RED=[91m"
set "CYAN=[96m"
set "BOLD=[1m"
set "NC=[0m"

echo %BOLD%╔══════════════════════════════════════════════════╗%NC%
echo %BOLD%║      DeepSeek Zoograf Client — Windows Setup    ║%NC%
echo %BOLD%║      HERO UI POR — Agentic Terminal Client      ║%NC%
echo %BOLD%╚══════════════════════════════════════════════════╝%NC%
echo.

:: ── Step 1: Check Python ────────────────────
echo %CYAN%[1/5]%NC% Checking Python installation...

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo %RED%[✗] Python not found!%NC%
    echo.
    echo   Download Python 3.10+ from:
    echo   %CYAN%https://www.python.org/downloads/%NC%
    echo.
    echo   ⚠ Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

python --version 2>&1 | findstr /R "3\.1[0-9]\." >nul
if %errorlevel% neq 0 (
    echo %YELLOW%[!] Warning: Python version may be below 3.10%NC%
    python --version
    echo   The tool requires Python 3.10 or higher.
    choice /c YN /m "Continue anyway?"
    if !errorlevel! equ 2 exit /b 1
) else (
    echo %GREEN%[✓]%NC% Python detected:
    for /f "tokens=*" %%a in ('python --version 2^>^&1') do echo     %%a
)

echo.

:: ── Step 2: Create virtual environment ──────
echo %CYAN%[2/5]%NC% Setting up virtual environment...

if exist "venv\" (
    echo %YELLOW%[!] Virtual environment already exists%NC%
    choice /c YN /m "Recreate it?"
    if !errorlevel! equ 1 (
        rmdir /s /q venv
        echo     Recreating...
        python -m venv venv
    )
) else (
    python -m venv venv
)

if %errorlevel% neq 0 (
    echo %RED%[✗] Failed to create virtual environment%NC%
    pause
    exit /b 1
)
echo %GREEN%[✓]%NC% Virtual environment created

:: ── Step 3: Install dependencies ────────────
echo.
echo %CYAN%[3/5]%NC% Installing Python dependencies...
echo     This may take a minute...

call venv\Scripts\activate.bat >nul 2>&1

python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo %RED%[✗] Failed to install some dependencies%NC%
    pause
    exit /b 1
)
echo %GREEN%[✓]%NC% All dependencies installed

:: ── Step 4: Configure API key ───────────────
echo.
echo %CYAN%[4/5]%NC% API Key configuration...

if not exist ".env" (
    copy .env.example .env >nul
    echo %YELLOW%[!]%NC% Created .env from .env.example
    echo     %BOLD%IMPORTANT:%NC% You need to set your DeepSeek API key.
    echo.
    echo     1. Open %BOLD%.env%NC% in a text editor
    echo     2. Replace %YELLOW%sk-your-key-here%NC% with your actual API key
    echo     3. Save the file
    echo.
    echo     Get a key at: %CYAN%https://platform.deepseek.com/api_keys%NC%
    echo.
    notepad .env
) else (
    echo %GREEN%[✓]%NC% .env already exists
)

:: ── Step 5: Verify installation ─────────────
echo.
echo %CYAN%[5/5]%NC% Verifying installation...

python -c "import textual; import openai; import rich; print('[✓] All imports OK')" 2>&1 | findstr /V "^$"
if %errorlevel% neq 0 (
    echo %RED%[✗] Verification failed%NC%
    pause
    exit /b 1
)

echo.
echo %GREEN%%BOLD%╔══════════════════════════════════════════════════╗%NC%
echo %GREEN%%BOLD%║  ✅  Setup Complete!                           ║%NC%
echo %GREEN%%BOLD%╠══════════════════════════════════════════════════╣%NC%
echo %GREEN%%BOLD%║                                                 ║%NC%
echo %GREEN%%BOLD%║  Run the client:                                ║%NC%
echo %GREEN%%BOLD%║     %CYAN%run.bat%NC%                              %GREEN%%BOLD%║%NC%
echo %GREEN%%BOLD%║     or                                           ║%NC%
echo %GREEN%%BOLD%║     %CYAN%call venv\Scripts\activate ^&^& python main.py%NC%   %GREEN%%BOLD%║%NC%
echo %GREEN%%BOLD%║                                                 ║%NC%
echo %GREEN%%BOLD%╚══════════════════════════════════════════════════╝%NC%
echo.

pause
