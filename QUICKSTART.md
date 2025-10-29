# Quick Start Guide

Get the OMEGA Trading Bot running in minutes!

## 🚀 Quick Install (Linux/Mac)

```bash
# Clone the repository
git clone https://github.com/fxgeniusllc-oss/OMEGA.git
cd OMEGA

# Run installation script
bash scripts/install.sh

# Edit configuration
nano .env

# Run demo
source venv/bin/activate
python scripts/demo.py
```

## 🪟 Quick Install (Windows)

```cmd
# Clone the repository
git clone https://github.com/fxgeniusllc-oss/OMEGA.git
cd OMEGA

# Run installation script
scripts\install.bat

# Edit configuration
notepad .env

# Run demo
venv\Scripts\activate.bat
python scripts\demo.py
```

## ⚙️ Configuration

Edit `.env` with your settings:

```env
# Essential Settings
MODE=DEV                              # DEV or LIVE
AUTO_START_ARBITRAGE=true             # Auto-start trading
ACTIVE_STRATEGIES=CROSS_CHAIN_ARBITRAGE,BRIDGE_ARBITRAGE

# For Live Trading (Optional)
INFURA_POLYGON_RPC=https://polygon-mainnet.g.alchemy.com/v2/YOUR_KEY
BOT_ADDRESS=0x...
PRIVATE_KEY=your_private_key_here

# Risk Management
MIN_PROFIT_USD=15
MIN_LIQUIDITY_USD=50000
```

## 🎮 Running the Bot

### Demo Mode (Safe - No Real Trades)

```bash
# Shows terminal output features
python scripts/demo.py
```

### Full Bot (Simulation Mode)

```bash
# Runs continuously, no real trades
python -m src.bot
```

### Full Bot (Live Trading)

⚠️ **WARNING**: This executes real trades with real money!

```bash
# Edit .env first:
# - Set LIVE_EXECUTION=true
# - Add your PRIVATE_KEY
# - Add RPC URLs

python -m src.bot
```

## 📊 What You'll See

### 1. Price Comparison Tables
```
============================================================
           PRICE COMPARISON - POLYGON | USDC/WETH           
============================================================
Source               Price                Liquidity            Spread%        
Uniswap V3          $1850.50000000        500,000.00           0.0950
QuickSwap           $1850.60000000        450,000.00           
```

### 2. Execution Results
```
==============================================================================
                              EXECUTION RESULTS                               
==============================================================================
Transaction Hash: 0x1a2b3c4d5e6f...
Net Profit: $72.85
ROI: 0.3925%
```

### 3. Trading Statistics
```
==============================================================================
                              TRADING STATISTICS                              
==============================================================================
Total Trades: 5
Win Rate: 80.00%
Net Profit: $313.65
```

## 🎨 Color Guide

- 🟢 **Green** = Profits, successful trades
- 🔴 **Red** = Losses, errors
- 🔵 **Blue** = Transaction hashes, blockchain info
- 🟦 **Cyan** = Price data, debug info
- 🟡 **Yellow** = Warnings

## 📝 Logging

Logs are saved to:
- **Console**: Real-time colored output
- **File**: `trading_bot.log` (plain text)

Check logs:
```bash
# Linux/Mac
tail -f trading_bot.log

# Windows
type trading_bot.log
```

## 🧪 Testing

Run tests to ensure everything works:

```bash
pytest tests/ -v
```

## 🛠️ Troubleshooting

### Issue: Module not found
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate.bat # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: No colors in terminal
```bash
# Install colorama
pip install colorama
```

### Issue: RPC connection failed
- Check your RPC URL in `.env`
- Verify API key is valid
- Try a different RPC provider

### Issue: No opportunities found
- This is normal - opportunities are rare
- Adjust `MIN_PROFIT_USD` in `.env` to be lower
- Enable more strategies in `ACTIVE_STRATEGIES`

## 📚 Next Steps

1. **Read** [FEATURES.md](FEATURES.md) for detailed feature documentation
2. **Check** [README.md](README.md) for complete installation guide
3. **Review** `.env.example` for all configuration options
4. **Explore** `src/` directory to understand the code

## 💡 Tips

1. **Start with Demo**: Always run `scripts/demo.py` first
2. **Test in DEV**: Use `MODE=DEV` before going live
3. **Small Amounts**: Start with small trade sizes
4. **Monitor Logs**: Watch both console and log files
5. **Set Alerts**: Configure Telegram notifications

## 🔐 Security

⚠️ **Never commit these files:**
- `.env` (contains private keys)
- `trading_bot.log` (may contain sensitive data)

✅ **Do this:**
- Use `.env.example` as template
- Keep `.gitignore` updated
- Secure your private keys
- Use hardware wallets for large amounts

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/fxgeniusllc-oss/OMEGA/issues)
- **Discussions**: [GitHub Discussions](https://github.com/fxgeniusllc-oss/OMEGA/discussions)
- **Documentation**: [FEATURES.md](FEATURES.md)

## ✅ Checklist

Before running the bot:

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created and configured
- [ ] RPC URLs added (for live trading)
- [ ] Private key secured (for live trading)
- [ ] Demo tested successfully
- [ ] Tests passing (`pytest tests/`)
- [ ] Logs directory created
- [ ] Risk parameters set in `.env`

## 🎯 Quick Commands

```bash
# Install
bash scripts/install.sh

# Run demo
python scripts/demo.py

# Run bot
python -m src.bot

# Run tests
pytest tests/ -v

# View logs
tail -f trading_bot.log

# Stop bot
Ctrl+C
```

Happy trading! 🚀
