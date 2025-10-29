@echo off
REM Run script for Windows

echo =========================================
echo DeFi Trading Bot - Startup Script
echo =========================================

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
python -c "import web3" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Check if .env file exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Copying .env.example to .env...
    copy .env.example .env
    echo Please edit .env with your configuration before running the bot.
    exit /b 1
)

REM Run the bot
echo Starting trading bot...
python -m src.bot
