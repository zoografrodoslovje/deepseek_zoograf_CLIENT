@echo off
title DeepSeek Zoograf Client - Setup
chcp 65001 >nul

:: ─────────────────────────────────────────────
:: DeepSeek Zoograf Client — Windows Installer
:: ─────────────────────────────────────────────
:: For PowerShell, run:   .\install.ps1
:: For CMD, run:          install.bat
:: ─────────────────────────────────────────────

setlocal enabledelayedexpansion

set "LINE=-------------------------------------------"

echo %LINE%
echo  DeepSeek Zoograf Client - Setup
echo  HERO UI POR - Agentic Terminal Client
echo %LINE%
echo.

:: ── Step 1: Check Python ────────────────────
echo [1/5] Checking Python installation...

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Python not found!
    echo.
    echo   Download Python 3.10+ from:
    echo   https://www.python.org/downloads/
    echo.
    echo   Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

python --version 2>&1 | findstr /R "3\.[1-9][0-9]\." >nul
if %errorlevel% neq 0 (
    echo [!] Warning: Python version may be below 3.10
    python --version
    choice /c YN /m "Continue anyway?"
    if !errorlevel! equ 2 exit /b 1
) else (
    echo [V] Python detected:
    for /f "tokens=*" %%a in ('python --version 2^>^&1') do echo     %%a
)

echo.

:: ── Step 2: Create virtual environment ──────
echo [2/5] Setting up virtual environment...

if exist "venv\" (
    echo [!] Virtual environment already exists
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
    echo [X] Failed to create virtual environment
    pause
    exit /b 1
)
echo [V] Virtual environment created

:: ── Step 3: Install dependencies ────────────
echo.
echo [3/5] Installing Python dependencies...
echo     This may take a minute...

call venv\Scripts\activate.bat >nul 2>&1

python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [X] Failed to install some dependencies
    pause
    exit /b 1
)
echo [V] All dependencies installed

:: ── Step 4: Configure API key ───────────────
echo.
echo [4/5] API Key configuration...

if not exist ".env" (
    copy .env.example .env >nul
    echo [!] Created .env from .env.example
    echo     IMPORTANT: You need to set your DeepSeek API key.
    echo.
    echo     1. Open .env in a text editor
    echo     2. Replace "sk-your-key-here" with your actual API key
    echo     3. Save the file
    echo.
    echo     Get a key at: https://platform.deepseek.com/api_keys
    echo.
    notepad .env
) else (
    echo [V] .env already exists
)

:: ── Step 5: Verify installation ─────────────
echo.
echo [5/5] Verifying installation...

python -c "import textual; import openai; import rich; print('[V] All imports OK')" 2>&1 | findstr /V "^$"

echo.
echo %LINE%
echo  Setup Complete!
echo %LINE%
echo.
echo  Run the client:
echo     .\run.bat
echo     or
echo     venv\Scripts\activate ^&^& python main.py
echo.
echo  NOTE: In PowerShell, use .\run.bat (not just run.bat)
echo.

pause
