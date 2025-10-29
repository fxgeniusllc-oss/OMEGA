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
=========================================
UNIFIED TRADING BOT STARTED
=========================================
Mode: DEV
Enabled Strategies: cross_chain_arbitrage, bridge_arbitrage
Auto-Start: true
Min Profit USD: $15.00
=========================================

✓ Connected to POLYGON: https://polygon-mainnet...
✓ Blockchain Interface Initialized
  Bot Address: 0x5548482e7ddd270e738b1e91994fa40ddb630461
  Executor Address: 0xb60CA70A37198A7A74D6231B2F661fAb707f75eF
  Connected Chains: polygon
  Active DEXs: quickswap, uniswap_v3, sushiswap, balancer, curve

================================================================================
Scan Iteration #1
================================================================================

[CROSS-CHAIN ARBITRAGE] Scanning ALL DEX sources for opportunities...

====================================================================================
PRICE COMPARISON - POLYGON | WETH/USDC (ALL VALUES IN USD)
====================================================================================
DEX/Source               Type         Price USD            Token A USD          ...
------------------------------------------------------------------------------------
QUICKSWAP                DEX          $1850.50000000       $2347.50000000       ...
UNISWAP_V3               DEX          $1850.93000000       $2347.50000000       ...
...
```

## Testing (Dev Mode)

The bot runs in **DEV mode** by default, which:
- ✓ Scans for opportunities
- ✓ Logs detailed information
- ✗ Does NOT execute real trades
- ✓ Simulates transaction results

Perfect for testing without risk!

## Switching to Live Mode

**⚠️ ONLY after thorough testing! ⚠️**

1. Test in DEV mode for at least 24 hours
2. Verify opportunities are being found
3. Check that gas calculations are accurate
4. Ensure you have sufficient funds in your wallet
5. Update `.env`:
```bash
MODE=LIVE
```

## Monitoring

### View Logs
```bash
# Real-time log following
tail -f trading_bot.log

# Last 100 lines
tail -n 100 trading_bot.log

# Search for profits
grep "Net Profit" trading_bot.log
```

### Check Stats
The bot displays statistics after each scan:
```
================================================================================
BOT STATISTICS
================================================================================
Total Trades: 5
Successful: 4
Failed: 1
Total Profit (USD): $127.34
================================================================================
```

## Stopping the Bot

### Graceful Shutdown
Press `Ctrl+C` in the terminal running the bot.

### Docker
```bash
docker-compose down
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'web3'"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### "Failed to connect to polygon"
**Solution:** Check your RPC URL in `.env`
```bash
# Verify URL is correct and has a valid API key
INFURA_POLYGON_RPC=https://polygon-mainnet.g.alchemy.com/v2/YOUR_KEY
```

### "No opportunities found"
**Solution:** Lower profit threshold or enable more DEXs
```bash
MIN_PROFIT_USD=5  # Lower threshold
ACTIVE_DEXS=quickswap,uniswap_v3,sushiswap,balancer,curve,paraswap,oneinch
```

### "Private key error"
**Solution:** Ensure private key is correctly formatted
```bash
# Must start with 0x and be 64 hex characters
PRIVATE_KEY=0x1234567890abcdef...
```

## Safety Checklist

Before running in LIVE mode:

- [ ] Tested in DEV mode for 24+ hours
- [ ] `.env` file is properly configured
- [ ] Private key is secure and never committed to git
- [ ] Wallet has sufficient funds for gas
- [ ] RPC providers are working
- [ ] MIN_PROFIT_USD is set appropriately
- [ ] MAX_TRADE_SIZE_USD is set conservatively
- [ ] Monitoring/alerts are configured
- [ ] Backup RPC URLs are configured
- [ ] You understand the risks

## Getting Help

1. **Read the documentation**: See `DOCUMENTATION.md`
2. **Check logs**: Review `trading_bot.log`
3. **Test configuration**: Run in SIM mode first
4. **Review code**: The bot is open source

## Next Steps

1. ✅ Install the bot
2. ✅ Configure `.env`
3. ✅ Run in DEV mode
4. ✅ Monitor for 24 hours
5. ⏸️ Optimize settings
6. ⏸️ Switch to LIVE mode (when ready)

## Important Notes

- **Start small**: Begin with low MAX_TRADE_SIZE_USD
- **Test thoroughly**: Use DEV mode extensively
- **Monitor closely**: Check logs regularly
- **Have backups**: Multiple RPC providers
- **Security first**: Never share your private key

---

**Ready to start?** Run `bash scripts/install.sh` (Linux/Mac) or `scripts\install.bat` (Windows)!
