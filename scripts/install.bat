@echo off
REM Quick installation script for Windows

echo ===============================================
echo   OMEGA Trading Bot - Installation Script
echo ===============================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    exit /b 1
)

echo ✓ Python found

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env from example
if not exist .env (
    echo.
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo ✓ .env created - please edit with your configuration
)

echo.
echo ===============================================
echo   Installation Complete!
echo ===============================================
echo.
echo To run the demo:
echo   venv\Scripts\activate.bat
echo   python scripts\demo.py
echo.
echo To run the bot:
echo   venv\Scripts\activate.bat
echo   python -m src.bot
echo.
pause
