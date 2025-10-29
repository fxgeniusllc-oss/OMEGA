@echo off
REM Run script for Windows

echo ==================================
echo DeFi Trading Bot - Starting
echo ==================================

REM Check if virtual environment exists
if not exist venv (
    echo Error: Virtual environment not found
    echo Please run: scripts\install.bat
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if .env exists
if not exist .env (
    echo Error: .env file not found
    echo Please copy .env.example to .env and configure it
    exit /b 1
)

REM Run the bot
python -m src.bot
