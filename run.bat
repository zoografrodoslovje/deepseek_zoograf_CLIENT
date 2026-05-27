@echo off
title DeepSeek Zoograf Client
chcp 65001 >nul

:: ─────────────────────────────────────────────
:: DeepSeek Zoograf Client — Quick Launcher
:: ─────────────────────────────────────────────

if not exist "venv\" (
    echo ╔══════════════════════════════════════════════════╗
    echo ║  Please run install.bat first to set up the     ║
    echo ║  virtual environment and install dependencies.  ║
    echo ╚══════════════════════════════════════════════════╝
    pause
    exit /b 1
)

if not exist ".env" (
    echo ╔══════════════════════════════════════════════════╗
    echo ║  No .env file found!                            ║
    echo ║                                                ║
    echo ║  Please copy .env.example to .env and set your  ║
    echo ║  DeepSeek API key before running the client.    ║
    echo ╚══════════════════════════════════════════════════╝
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
python main.py
if %errorlevel% neq 0 (
    echo.
    echo ╔══════════════════════════════════════════════════╗
    echo ║  Client exited with error code %errorlevel%             ║
    echo ║  Check TROUBLESHOOTING.md for help.              ║
    echo ╚══════════════════════════════════════════════════╝
    pause
)
