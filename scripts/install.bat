@echo off
REM Installation script for Windows

echo Installing DeFi Trading Bot...

REM Create virtual environment
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Upgrade pip
python -m pip install --upgrade pip setuptools wheel

REM Install dependencies
pip install -r requirements.txt

REM Create .env file from example if it doesn't exist
if not exist .env (
    copy .env.example .env
    echo Created .env file. Please edit it with your configuration.
)

REM Create logs directory
if not exist logs mkdir logs

echo Installation complete!
echo Please edit .env with your configuration, then run: scripts\run.bat
