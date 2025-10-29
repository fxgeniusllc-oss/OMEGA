#!/bin/bash
# Run script for Linux/Mac

echo "Starting DeFi Trading Bot..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the bot
python -m src.bot
