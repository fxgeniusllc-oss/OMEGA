#!/bin/bash
# Installation script for Linux/Mac

echo "=================================="
echo "DeFi Trading Bot - Installation"
echo "=================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

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
python -m pip install --upgrade pip setuptools wheel

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your actual keys and addresses"
fi

echo ""
echo "=================================="
echo "✅ Installation complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Edit .env with your configuration:"
echo "   nano .env"
echo ""
echo "2. Activate virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "3. Run the bot:"
echo "   python -m src.bot"
echo ""
