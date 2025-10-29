@echo off
REM Installation script for Windows

echo =========================================
echo DeFi Trading Bot - Installation Script
echo =========================================

REM Check Python version
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Copy .env.example if .env doesn't exist
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo [92m[SUCCESS][0m .env file created. Please edit it with your configuration.
) else (
    echo [92m[SUCCESS][0m .env file already exists.
)

REM Create log directory
if not exist "logs\" mkdir logs
echo [92m[SUCCESS][0m Log directory created.

REM Create models directory
if not exist "models\" mkdir models
echo [92m[SUCCESS][0m Models directory created.

echo.
echo =========================================
echo Installation Complete!
echo =========================================
echo Next steps:
echo 1. Edit .env with your API keys and configuration
echo 2. Run: scripts\run.bat
echo =========================================
pause
