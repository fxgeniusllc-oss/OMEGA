@echo off
REM Run script for Windows

echo Starting DeFi Trading Bot...

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Run the bot
python -m src.bot
