#!/bin/bash
# Run script for Linux/Mac

echo "=================================="
echo "DeFi Trading Bot - Starting"
echo "=================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found"
    echo "Please run: bash scripts/install.sh"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f .env ]; then
    echo "Error: .env file not found"
    echo "Please copy .env.example to .env and configure it"
    exit 1
fi

# Run the bot
python -m src.bot
