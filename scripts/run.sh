#!/bin/bash
# Run script for Linux/Mac

echo "========================================="
echo "DeFi Trading Bot - Startup Script"
echo "========================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import web3" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found!"
    echo "Copying .env.example to .env..."
    cp .env.example .env
    echo "Please edit .env with your configuration before running the bot."
    exit 1
fi

# Run the bot
echo "Starting trading bot..."
python -m src.bot
