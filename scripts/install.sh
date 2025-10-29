#!/bin/bash
# Quick installation and demo script for Linux/Mac

echo "==============================================="
echo "  OMEGA Trading Bot - Installation Script"
echo "==============================================="
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "✓ Python 3 found"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env from example
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "✓ .env created - please edit with your configuration"
fi

echo ""
echo "==============================================="
echo "  Installation Complete!"
echo "==============================================="
echo ""
echo "To run the demo:"
echo "  source venv/bin/activate"
echo "  python scripts/demo.py"
echo ""
echo "To run the bot:"
echo "  source venv/bin/activate"
echo "  python -m src.bot"
echo ""
