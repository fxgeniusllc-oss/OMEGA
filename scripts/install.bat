@echo off
REM Installation script for Windows

echo ==================================
echo DeFi Trading Bot - Installation
echo ==================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed
    exit /b 1
)

echo Python found:
python --version

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
python -m pip install --upgrade pip setuptools wheel

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env if it doesn't exist
if not exist .env (
    echo.
    echo Creating .env file from template...
    copy .env.example .env
    echo WARNING: Please edit .env with your actual keys and addresses
)

echo.
echo ==================================
echo Installation complete!
echo ==================================
echo.
echo Next steps:
echo 1. Edit .env with your configuration:
echo    notepad .env
echo.
echo 2. Activate virtual environment:
echo    venv\Scripts\activate.bat
echo.
echo 3. Run the bot:
echo    python -m src.bot
echo.
pause
