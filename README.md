# OMEGA - Unified DeFi Trading Bot

A production-ready, multi-strategy DeFi trading bot with advanced features including MEV detection, cross-chain arbitrage, AI-powered predictions, and comprehensive risk management.

## 🎯 Key Features

### Unified Architecture
- **Single UnifiedTradingBot class** that orchestrates all strategies
- Each strategy has its own specialized engine class (MempoolWatcher, CrossChainArbitrageur, etc.)
- **Configuration-driven approach** - enable/disable strategies via environment variables
- Works across **multiple chains** (Polygon, Ethereum, Arbitrum, Optimism)

### 9 Integrated Trading Strategies

1. **Mempool Watching** - MEV detection and sandwich trading
2. **Cross-Chain Arbitrage** - Price differences across networks
3. **Pump Prediction AI** - Technical analysis (RSI included)
4. **Market Making** - Bid-ask spread optimization
5. **Statistical Arbitrage** - Correlation-based mean reversion
6. **Gamma Scalping** - Hedging and rehedging logic
7. **Funding Rate Harvesting** - Perpetual futures arbitrage
8. **Volatility Arbitrage** - Realized vs implied vol trading
9. **Bridge Arbitrage** - Cross-bridge price differences

### Advanced Features

- **Position Manager** - Enforces Kelly Criterion sizing and risk limits
- **Flash Loan Manager** - Handles Balancer/Aave flash loans with fee calculation
- **Opportunity Ranking** - Sorts by profit * confidence
- **Multi-mode Support** - LIVE, DEV, or SIM (simulation) trading
- **Comprehensive Logging** - Track all decisions and executions
- **Error Handling** - Graceful failures per strategy

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip
- Virtual environment (recommended)

### Installation

**Linux/Mac:**
```bash
bash scripts/install.sh
```

**Windows:**
```bash
scripts\install.bat
```

**Manual Installation:**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your configuration
```

### Configuration

Edit `.env` with your settings:

```env
# Trading Mode: LIVE, DEV, or SIM
MODE=SIM

# Blockchain RPCs
INFURA_POLYGON_RPC=https://polygon-rpc.com
INFURA_ETHEREUM_RPC=https://eth-rpc.com
INFURA_ARBITRUM_RPC=https://arb-rpc.com
INFURA_OPTIMISM_RPC=https://op-rpc.com

# Active Strategies (comma-separated)
ACTIVE_STRATEGIES=MEMPOOL_WATCHING,CROSS_CHAIN_ARBITRAGE,PUMP_PREDICTION,MARKET_MAKING,STATISTICAL_ARBITRAGE,GAMMA_SCALPING,FUNDING_RATE,VOLATILITY_ARBITRAGE,BRIDGE_ARBITRAGE

# Risk Management
MAX_POSITION_SIZE=10000
RISK_PER_TRADE=0.02
SLIPPAGE_TOLERANCE=0.005
GAS_PRICE_MULTIPLIER=1.1

# Flash Loan Provider: BALANCER or AAVE
FLASH_LOAN_PROVIDER=BALANCER
```

### Running the Bot

**Linux/Mac:**
```bash
bash scripts/run.sh
```

**Windows:**
```bash
scripts\run.bat
```

**Direct Python:**
```bash
python bot.py
# or
python -m src.bot
```

---

## 📊 Trading Modes

### SIM Mode (Simulation)
- Uses mock data and mock capital ($100,000)
- No real transactions
- Perfect for testing and development
```env
MODE=SIM
```

### DEV Mode (Development)
- Connects to real blockchain RPCs
- Uses real data but can limit execution
- For testing with live data
```env
MODE=DEV
LIVE_EXECUTION=false
```

### LIVE Mode (Production)
- Real trading with real funds
- Requires PRIVATE_KEY configuration
- ⚠️ Use with caution!
```env
MODE=LIVE
PRIVATE_KEY=your_private_key_here
LIVE_EXECUTION=true
```

---

## 🧪 Testing

Run the test suite:
```bash
pip install pytest pytest-asyncio
pytest tests/ -v
```

Run specific tests:
```bash
pytest tests/test_bot.py -v
```

---

## 🐳 Docker Deployment

### Build and Run
```bash
cd docker
docker-compose up -d
```

### View Logs
```bash
docker-compose logs -f bot
```

### Stop Bot
```bash
docker-compose down
```

---

## 📁 Project Structure

```
```
OMEGA/
│
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── .env.example                   # Example environment variables
├── .env                          # Your config (DO NOT COMMIT)
├── .gitignore                    # Git ignore rules
├── bot.py                        # Convenience run script
│
├── src/
│   ├── __init__.py
│   ├── bot.py                    # Main UnifiedTradingBot class
│   ├── config.py                 # Configuration management
│   ├── logger.py                 # Logging setup
│   ├── oracle.py                 # Price oracle
│   ├── blockchain.py             # Blockchain interface
│   ├── position_manager.py       # Position & risk management
│   ├── flash_loan_manager.py     # Flash loan handling
│   │
│   ├── strategies/
│   │   ├── __init__.py
│   │   ├── base.py               # Base strategy class
│   │   ├── mempool.py            # MEV & sandwich attacks
│   │   ├── arbitrage.py          # Cross-chain arbitrage
│   │   ├── bridge.py             # Bridge arbitrage
│   │   ├── pump_prediction.py    # AI pump prediction
│   │   ├── market_making.py      # Market making
│   │   ├── statistical_arbitrage.py  # Stat arb
│   │   ├── gamma_scalping.py     # Gamma scalping
│   │   ├── funding_rate.py       # Funding rate harvest
│   │   └── volatility_arbitrage.py   # Vol arbitrage
│   │
│   └── utils/
│       ├── __init__.py
│       ├── constants.py          # Constants & enums
│       └── helpers.py            # Utility functions
│
├── tests/
│   ├── __init__.py
│   └── test_bot.py               # Bot tests
│
├── scripts/
│   ├── run.sh                    # Linux/Mac run script
│   ├── run.bat                   # Windows run script
│   ├── install.sh                # Linux/Mac installer
│   └── install.bat               # Windows installer
│
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── .dockerignore
│
├── logs/                         # Log files (auto-created)
└── models/                       # ML models (optional)
```

---

## 🔧 Strategy Configuration

Enable/disable strategies by editing `ACTIVE_STRATEGIES` in `.env`:

```env
# Enable all strategies
ACTIVE_STRATEGIES=MEMPOOL_WATCHING,CROSS_CHAIN_ARBITRAGE,PUMP_PREDICTION,MARKET_MAKING,STATISTICAL_ARBITRAGE,GAMMA_SCALPING,FUNDING_RATE,VOLATILITY_ARBITRAGE,BRIDGE_ARBITRAGE

# Enable only arbitrage strategies
ACTIVE_STRATEGIES=CROSS_CHAIN_ARBITRAGE,BRIDGE_ARBITRAGE

# Enable only AI and statistical strategies
ACTIVE_STRATEGIES=PUMP_PREDICTION,STATISTICAL_ARBITRAGE,VOLATILITY_ARBITRAGE
```

---

## 💰 Risk Management

The bot includes comprehensive risk management:

### Kelly Criterion Position Sizing
```python
position_size = kelly_fraction * capital
# Capped at MAX_POSITION_SIZE
```

### Risk Limits
- `MAX_POSITION_SIZE`: Maximum size per trade
- `RISK_PER_TRADE`: Maximum risk per trade (as fraction of capital)
- `SLIPPAGE_TOLERANCE`: Maximum acceptable slippage

### Flash Loan Safety
- Automatic fee calculation
- Profitability check before execution
- Provider selection (Balancer/Aave)

---

## 📈 Performance Monitoring

The bot logs all activity to:
- Console (color-coded)
- `trading_bot.log` file

### Example Output
```
2025-10-29 16:01:51 [INFO] ================================================================================
2025-10-29 16:01:51 [INFO] Initializing Unified Trading Bot
2025-10-29 16:01:51 [INFO] Mode: SIM
2025-10-29 16:01:51 [INFO] ================================================================================
2025-10-29 16:01:51 [INFO] ✓ Strategy enabled: MEMPOOL_WATCHING
2025-10-29 16:01:51 [INFO] ✓ Strategy enabled: CROSS_CHAIN_ARBITRAGE
...
2025-10-29 16:01:51 [INFO] Trading bot started
2025-10-29 16:01:51 [INFO] Capital updated: $100000.00
2025-10-29 16:01:51 [INFO] Found 11 opportunities
2025-10-29 16:01:51 [INFO] Position size calculated for MempoolWatcher: $8000.00 (Win prob: 70.00%)
2025-10-29 16:01:51 [INFO] Executing opportunity: MempoolWatcher | Profit $120.00 | Confidence 70.00%
2025-10-29 16:01:51 [INFO] ✓ Trade executed successfully | Profit $120.00
2025-10-29 16:01:52 [INFO] Executed 5 trades this cycle
2025-10-29 16:01:52 [INFO] Total profit: $420.00
```

---

## 🔐 Security Best Practices

1. **Never commit `.env` file** - It contains sensitive keys
2. **Use hardware wallet** for LIVE mode if possible
3. **Start with SIM mode** - Test thoroughly before live trading
4. **Use small amounts** initially in LIVE mode
5. **Monitor gas prices** - High gas can eat profits
6. **Set conservative risk limits** - Better safe than sorry
7. **Keep private keys secure** - Never share or expose

---

## 🛠️ Troubleshooting

### Bot not finding opportunities
- Check `MODE` is set to `SIM` for testing
- Verify strategies are enabled in `ACTIVE_STRATEGIES`
- Check logs for errors

### RPC connection issues
- Verify RPC URLs in `.env`
- Check if RPC provider is working
- Try alternative RPC endpoints

### Installation issues
```bash
# Upgrade pip
pip install --upgrade pip

# Install specific versions
pip install web3==6.11.3 python-dotenv==1.0.0 aiohttp==3.9.1
```

### Import errors
```bash
# Make sure you're in the project root
cd /path/to/OMEGA

# Run with module syntax
python -m src.bot
```

---

## 📚 Environment Variables Reference
## 📚 Environment Variables Reference

### Trading Mode
| Variable | Values | Description |
|----------|--------|-------------|
| `MODE` | `LIVE`, `DEV`, `SIM` | Trading mode |
| `AUTO_START_ARBITRAGE` | `true`, `false` | Auto-start on launch |
| `LIVE_EXECUTION` | `true`, `false` | Execute real trades |

### Addresses & Keys
| Variable | Description |
|----------|-------------|
| `BOT_ADDRESS` | Your wallet address |
| `PRIVATE_KEY` | Private key (LIVE mode only) |

### RPC Endpoints
| Variable | Description |
|----------|-------------|
| `INFURA_POLYGON_RPC` | Polygon RPC URL |
| `INFURA_ETHEREUM_RPC` | Ethereum RPC URL |
| `INFURA_ARBITRUM_RPC` | Arbitrum RPC URL |
| `INFURA_OPTIMISM_RPC` | Optimism RPC URL |

### Strategy Configuration
| Variable | Description |
|----------|-------------|
| `ACTIVE_STRATEGIES` | Comma-separated list of strategies |

### Risk Management
| Variable | Default | Description |
|----------|---------|-------------|
| `MAX_POSITION_SIZE` | `10000` | Max position size (USD) |
| `RISK_PER_TRADE` | `0.02` | Risk per trade (2% of capital) |
| `SLIPPAGE_TOLERANCE` | `0.005` | Max slippage (0.5%) |
| `GAS_PRICE_MULTIPLIER` | `1.1` | Gas price multiplier |

### Flash Loans
| Variable | Values | Description |
|----------|--------|-------------|
| `FLASH_LOAN_PROVIDER` | `BALANCER`, `AAVE` | Flash loan provider |

### Logging
| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_FILE` | `trading_bot.log` | Log file path |
| `LOG_LEVEL` | `INFO` | Log level |

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

## ⚠️ Disclaimer

**This bot is for educational purposes only.**

- Trading cryptocurrencies carries significant risk
- You may lose all your invested capital
- Past performance does not guarantee future results
- Always do your own research (DYOR)
- Test thoroughly in SIM mode before live trading
- The authors are not responsible for any financial losses

---

## 📄 License

This project is provided as-is for educational purposes.

---

## 🔗 Resources

- [Web3.py Documentation](https://web3py.readthedocs.io/)
- [Balancer Flash Loans](https://docs.balancer.fi/reference/contracts/flash-loans.html)
- [Aave Flash Loans](https://docs.aave.com/developers/guides/flash-loans)
- [Kelly Criterion](https://en.wikipedia.org/wiki/Kelly_criterion)

---

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check the troubleshooting section
- Review the logs in `trading_bot.log`

---

**Built with ❤️ for the DeFi community**
├── setup.py                            # Package installation script
├── .env.example                        # Example environment variables
├── .env                                # Your actual env (DO NOT COMMIT)
├── .gitignore                          # Git ignore file
│
├── src/
│   ├── __init__.py
│   ├── bot.py                          # Main trading bot (COPY FROM ARTIFACT)
│   ├── config.py                       # Configuration loader
│   ├── logger.py                       # Enhanced logging setup
│   ├── oracle.py                       # Price oracle & conversion
│   ├── blockchain.py                   # Blockchain interface
│   ├── strategies/
│   │   ├── __init__.py
│   │   ├── arbitrage.py                # Cross-chain arbitrage
│   │   ├── bridge.py                   # Bridge arbitrage
│   │   ├── mempool.py                  # Mempool watching
│   │   └── base.py                     # Base strategy class
│   └── utils/
│       ├── __init__.py
│       ├── helpers.py                  # Utility functions
│       └── constants.py                # Constants & enums
│
├── models/
│   ├── lstm_market_maker.h5            # Pre-trained LSTM (optional)
│   ├── catboost_profit_predictor.cbm   # CatBoost model (optional)
│   └── xgboost_risk_analyzer.xgb       # XGBoost model (optional)
│
├── logs/
│   ├── trading_bot.log                 # Main bot logs
│   └── trades_history.json             # Trade history
│
├── tests/
│   ├── __init__.py
│   ├── test_bot.py
│   ├── test_strategies.py
│   └── test_oracle.py
│
├── scripts/
│   ├── install.sh                      # Linux/Mac installation
│   ├── install.bat                     # Windows installation
│   ├── run.sh                          # Linux/Mac run script
│   ├── run.bat                         # Windows run script
│   └── backtest.py                     # Backtesting script
│
└── docker/
    ├── Dockerfile
    ├── docker-compose.yml
    └── .dockerignore
```

---

## 📦 Dependencies (requirements.txt)

```
# Core Web3 & Blockchain
web3==6.11.3
eth-account==0.10.0
eth-keys==0.5.1
eth-typing==4.1.0

# Async & HTTP
aiohttp==3.9.1
asyncio==3.4.3
requests==2.31.0

# Data & Math
python-dotenv==1.0.0
Decimal==1.0
numpy==1.24.3
pandas==2.0.3

# Machine Learning (Optional - for AI strategies)
torch==2.1.2
scikit-learn==1.3.2
catboost==1.2.2
xgboost==2.0.3

# Logging & Monitoring
colorlog==6.8.0
python-json-logger==2.0.7

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0

# Security
cryptography==41.0.7

# Deployment
gunicorn==21.2.0
```

---

## 🔧 Installation Guide (Windows with VENV)

### **Step 1: Clone Repository**
```bash
git clone https://github.com/yourusername/defi-trading-bot.git
cd defi-trading-bot
```

### **Step 2: Create Virtual Environment**

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```bash
python -m venv venv
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### **Step 3: Upgrade pip**
```bash
python -m pip install --upgrade pip setuptools wheel
```

### **Step 4: Install Dependencies**
```bash
pip install -r requirements.txt
```

Or for development (with testing tools):
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### **Step 5: Create .env File**
```bash
# Copy example env
copy .env.example .env

# Edit .env with your actual values
# (Use your favorite text editor)
```

### **Step 6: Verify Installation**
```bash
python -c "import web3; print(web3.__version__)"
python -c "import dotenv; print('dotenv installed')"
```

---

## 📝 .env.example File

Create `.env.example` in root:

```env
# ===== TRADING MODE =====
MODE=DEV
AUTO_START_ARBITRAGE=true
AUTO_TRADING_ENABLED=true
LIVE_EXECUTION=false

# ===== ADDRESSES =====
BOT_ADDRESS=0x5548482e7ddd270e738b1e91994fa40ddb630461
EXECUTOR_ADDRESS=0xb60CA70A37198A7A74D6231B2F661fAb707f75eF
PRIVATE_KEY=your_private_key_here

# ===== POLYGON RPC =====
INFURA_POLYGON_RPC=https://polygon-mainnet.g.alchemy.com/v2/YOUR_KEY
INFURA_POLYGON_RPC_WS=wss://polygon-mainnet.g.alchemy.com/v2/YOUR_KEY
QUICKNODE_RPC_URL=https://orbital-special-moon.matic.quiknode.pro/YOUR_KEY
ALCHEMY_RPC_URL=https://polygon-mainnet.g.alchemy.com/v2/YOUR_KEY

# ===== OTHER CHAINS RPC =====
ETHEREUM_RPC_URL=https://mainnet.infura.io/v3/YOUR_KEY
ARBITRUM_RPC_URL=https://arb-mainnet.g.alchemy.com/v2/YOUR_KEY
OPTIMISM_RPC_URL=https://opt-mainnet.g.alchemy.com/v2/YOUR_KEY
BASE_RPC_URL=https://base-mainnet.g.alchemy.com/v2/YOUR_KEY
BSC_RPC_URL=https://bsc-mainnet.g.alchemy.com/v2/YOUR_KEY

# ===== CHAIN CONFIGURATION =====
POLYGON_ENABLED=true
ETHEREUM_ENABLED=false
ARBITRUM_ENABLED=false
OPTIMISM_ENABLED=false
BASE_ENABLED=false

# ===== DEX ROUTERS =====
QUICKSWAP_ROUTER=0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff
SUSHISWAP_ROUTER=0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506
UNISWAP_V3_ROUTER=0xE592427A0AEce92De3Edee1F18E0157C05861564
PARASWAP_ROUTER=0xDEF171Fe48CF0115B1d80b88dc8eAB59176FEe57
ONEINCH_ROUTER=0x1111111254EEB25477B68fb85Ed929f73A960582
BALANCER_V2_VAULT=0xBA12222222228d8Ba445958a75a0704d566BF2C8
CURVE_ROUTER=0xB576491F1E6e5E62f1d8f26062Ee822b40B0E0d4

# ===== ACTIVE DEXs & STRATEGIES =====
ACTIVE_DEXS=quickswap,uniswap_v3,sushiswap,balancer,curve,paraswap,oneinch
ACTIVE_STRATEGIES=CROSS_CHAIN_ARBITRAGE,BRIDGE_ARBITRAGE

# ===== FLASH LOAN =====
FLASHLOAN_PROVIDER=BALANCER_VAULT
MAX_FLASHLOAN_PERCENT_POOL_TVL=10

# ===== TOKEN ADDRESSES (POLYGON) =====
WMATIC=0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270
USDC=0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174
USDT=0xc2132D05D31c914a87C6611C10748AEb04B58e8F
DAI=0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063
WETH=0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619
WBTC=0x1BFD67037B42Cf73acF2047067bd4F2C47D9BfD6

# ===== RISK MANAGEMENT =====
MIN_PROFIT_USD=15
MIN_LIQUIDITY_USD=50000
MAX_TRADE_SIZE_USD=2000000
MIN_TRADE_SIZE_USD=10000
SLIPPAGE_BPS=50
GAS_PRICE_MULTIPLIER=1.2

# ===== PERFORMANCE =====
SCAN_CYCLE_INTERVAL_MS=5000
MAX_CONCURRENT_SCANS=10
CONFIDENCE_THRESHOLD=0.55

# ===== API KEYS =====
POLYGONSCAN_API_KEY=your_key_here
COINGECKO_API_KEY=your_key_here
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# ===== LOGGING =====
LOG_FILE=trading_bot.log
LOG_LEVEL=INFO
```

---

## 🚀 Quick Start Commands

### **Windows (PowerShell)**

```powershell
# Setup
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env

# Edit .env with your config
notepad .env

# Run bot
python -m src.bot

# Or using run script
.\scripts\run.bat
```

### **Linux/Mac (Bash)**

```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# Edit .env
nano .env

# Run bot
python -m src.bot

# Or using run script
bash scripts/run.sh
```

---

## 📄 .gitignore File

```
# Virtual Environment
venv/
env/
ENV/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Environment Variables
.env
.env.local
.env.*.local

# Logs & Data
logs/
*.log
trades_history.json

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Testing
.pytest_cache/
.coverage
htmlcov/

# Models
models/*.h5
models/*.cbm
models/*.xgb

# OS
Thumbs.db
.DS_Store
```

---

## 🔍 Verify Installation

After installation, test everything works:

```bash
# Test 1: Import web3
python -c "from web3 import Web3; print('✓ Web3 OK')"

# Test 2: Import bot modules
python -c "from src.bot import UnifiedTradingBot; print('✓ Bot imports OK')"

# Test 3: Load environment
python -c "from dotenv import load_dotenv; load_dotenv(); print('✓ .env loaded OK')"

# Test 4: Run bot in SIM mode
python -m src.bot
```

---

## 🐳 Docker Setup (Optional)

### **Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "src.bot"]
```

### **docker-compose.yml**
```yaml
version: '3.8'
services:
  bot:
    build: .
    env_file: .env
    volumes:
      - ./logs:/app/logs
    restart: always
```

### **Run with Docker**
```bash
docker-compose up -d
docker-compose logs -f bot
```

---

## 📊 Requirements Breakdown

| Package | Purpose | Why Needed |
|---------|---------|-----------|
| `web3` | Blockchain interaction | Talk to Ethereum/Polygon |
| `aiohttp` | Async HTTP requests | Real-time price feeds |
| `python-dotenv` | Environment variables | Load .env config |
| `numpy/pandas` | Data processing | Analyze price data |
| `pytest` | Testing framework | Unit & integration tests |
| `colorlog` | Colored logging | Better terminal output |
| `torch` | Deep learning | Optional ML strategies |
| `cryptography` | Security | Encrypt sensitive data |

---

## ⚡ Installation Speed Tips

**Fastest install (Windows):**
```powershell
# Use pre-built wheels
pip install --only-binary :all: -r requirements.txt
```

**Without ML (faster):**
Create `requirements-lite.txt`:
```
web3==6.11.3
aiohttp==3.9.1
python-dotenv==1.0.0
requests==2.31.0
```

Then:
```bash
pip install -r requirements-lite.txt
```

---

## 🛠️ Troubleshooting

### **Issue: `ModuleNotFoundError: No module named 'web3'`**
```bash
# Solution:
pip install web3 --upgrade
```

### **Issue: `venv not activating on Windows`**
```powershell
# Solution (allow script execution):
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

### **Issue: `Python not found`**
```bash
# Verify Python is installed:
python --version
py --version  # Alternative on Windows
```

### **Issue: `.env not loading`**
```bash
# Verify .env exists in root directory:
ls .env          # Linux/Mac
dir .env         # Windows

# And it contains:
head -5 .env     # Linux/Mac
type .env        # Windows
```

---

## 📚 Next Steps After Installation

1. **Copy the bot code** from artifact → `src/bot.py`
2. **Edit `.env`** with your keys & addresses
3. **Test in DEV mode** first: `MODE=DEV`
4. **Run bot**: `python -m src.bot`
5. **Check logs**: `tail -f trading_bot.log` (or `type trading_bot.log` on Windows)

---

## 🎯 Production Deployment Checklist

- [ ] `.env` created with all required keys
- [ ] `MODE=LIVE` (or keep as `DEV` for testing)
- [ ] Private key secured (use hardware wallet if possible)
- [ ] Test run in `SIM` mode first
- [ ] Check logs for errors
- [ ] Monitor gas prices
- [ ] Set up alerts (Telegram, email)
- [ ] Have backup RPC URLs ready
- [ ] Test with small trade amounts first
