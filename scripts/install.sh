#!/bin/bash
# Installation script for Linux/Mac

echo "Installing DeFi Trading Bot..."

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install dependencies
pip install -r requirements.txt

# Create .env file from example if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Created .env file. Please edit it with your configuration."
fi

# Create logs directory
mkdir -p logs

echo "Installation complete!"
echo "Please edit .env with your configuration, then run: bash scripts/run.sh"
