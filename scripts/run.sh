#!/bin/bash
# Run the trading bot

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Run the bot
echo "Starting OMEGA Trading Bot..."
python -m src.bot
