@echo off
REM Run the trading bot

REM Check if virtual environment is activated
if "%VIRTUAL_ENV%"=="" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Run the bot
echo Starting OMEGA Trading Bot...
python -m src.bot
