#!/bin/bash
# Installation script for Linux/Mac

echo "========================================="
echo "DeFi Trading Bot - Installation Script"
echo "========================================="

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Copy .env.example if .env doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created. Please edit it with your configuration."
else
    echo "✓ .env file already exists."
fi

# Create log directory
mkdir -p logs
echo "✓ Log directory created."

# Create models directory
mkdir -p models
echo "✓ Models directory created."

echo ""
echo "========================================="
echo "Installation Complete!"
echo "========================================="
echo "Next steps:"
echo "1. Edit .env with your API keys and configuration"
echo "2. Run: bash scripts/run.sh"
echo "========================================="
