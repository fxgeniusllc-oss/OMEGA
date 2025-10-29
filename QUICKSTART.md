# OMEGA DeFi Bot - Quick Start Guide

## Installation (3 Minutes)

### Option 1: Automated Installation (Recommended)

**Linux/Mac:**
```bash
git clone https://github.com/fxgeniusllc-oss/OMEGA.git
cd OMEGA
bash scripts/install.sh
```

**Windows:**
```batch
git clone https://github.com/fxgeniusllc-oss/OMEGA.git
cd OMEGA
scripts\install.bat
```

### Option 2: Manual Installation

```bash
# Clone repository
git clone https://github.com/fxgeniusllc-oss/OMEGA.git
cd OMEGA

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate.bat  # Windows

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
```

## Configuration (5 Minutes)

Edit `.env` file with your settings:

### Minimal Configuration (Required)
```bash
# 1. Set your private key
PRIVATE_KEY=0xYOUR_PRIVATE_KEY_HERE

# 2. Set your bot address
BOT_ADDRESS=0xYOUR_WALLET_ADDRESS_HERE

# 3. Set at least one RPC URL
INFURA_POLYGON_RPC=https://polygon-mainnet.g.alchemy.com/v2/YOUR_KEY
```

### Recommended Configuration
```bash
# Enable multiple chains for better opportunities
POLYGON_ENABLED=true
ETHEREUM_ENABLED=true
ARBITRUM_ENABLED=true

# Add multiple RPC providers for redundancy
QUICKNODE_RPC_URL=https://...
ALCHEMY_RPC_URL=https://...

# Configure risk parameters
MIN_PROFIT_USD=15
MAX_TRADE_SIZE_USD=10000
SLIPPAGE_BPS=50
```

## Running the Bot

### Using Scripts (Easiest)

**Linux/Mac:**
```bash
bash scripts/run.sh
```

**Windows:**
```batch
scripts\run.bat
```

### Manual Run
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate.bat  # Windows

# Run bot
python -m src.bot
```

### Using Docker
```bash
# Build and start
cd docker
docker-compose up -d

# View logs
docker-compose logs -f bot

# Stop
docker-compose down
```

## What to Expect

When you run the bot, you'll see:

```
