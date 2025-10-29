# DeFi Trading Bot - OMEGA

## 🚀 Current Implementation Status

✅ **Hyper-Compact Transaction Engine** - Fully Implemented

The repository now includes a production-ready, modular transaction engine with the following features:

- **6 Core Modules**: Opportunity Ingest, Payload Encoder, Transaction Builder, Signer, Broadcast Engine, and ML Decision Engine
- **Pipeline Architecture**: Asynchronous queue-based processing for high performance
- **Thread-Safe**: Concurrent execution using Python threading
- **Security-First**: Broadcasting disabled by default, placeholder data for safe testing
- **Well-Documented**: Comprehensive documentation in `docs/TRANSACTION_ENGINE.md`
- **Tested**: Unit tests included in `tests/test_transaction_engine.py`
- **Example Scripts**: Ready-to-use examples in `scripts/`

### Quick Start

```bash
# Clone and setup
git clone https://github.com/fxgeniusllc-oss/OMEGA.git
cd OMEGA

# Install dependencies (optional, if you want to run)
pip install -r requirements.txt

# View the transaction engine
cat src/transaction_engine.py

# Read the documentation
cat docs/TRANSACTION_ENGINE.md

# Run example (requires web3 installation)
python scripts/run_transaction_engine.py
```

See [Transaction Engine Documentation](docs/TRANSACTION_ENGINE.md) for detailed information.

---

# DeFi Trading Bot - Repository Setup & Installation Guide

## 📁 Repository Structure

```
OMEGA/
│
├── README.md                           # Main documentation
├── requirements.txt                    # Python dependencies (✅ Implemented)
├── .env.example                        # Example environment variables (✅ Implemented)
├── .env                                # Your actual env (DO NOT COMMIT)
├── .gitignore                          # Git ignore file (✅ Implemented)
│
├── src/
│   ├── __init__.py                     # (✅ Implemented)
│   ├── transaction_engine.py           # Hyper-compact transaction engine (✅ Implemented)
│   ├── bot.py                          # Main trading bot (TO BE IMPLEMENTED)
│   ├── config.py                       # Configuration loader (TO BE IMPLEMENTED)
│   ├── logger.py                       # Enhanced logging setup (TO BE IMPLEMENTED)
│   ├── oracle.py                       # Price oracle & conversion (TO BE IMPLEMENTED)
│   ├── blockchain.py                   # Blockchain interface (TO BE IMPLEMENTED)
│   ├── strategies/
│   │   ├── __init__.py                 # (✅ Implemented)
│   │   ├── arbitrage.py                # Cross-chain arbitrage (TO BE IMPLEMENTED)
│   │   ├── bridge.py                   # Bridge arbitrage (TO BE IMPLEMENTED)
│   │   ├── mempool.py                  # Mempool watching (TO BE IMPLEMENTED)
│   │   └── base.py                     # Base strategy class (TO BE IMPLEMENTED)
│   └── utils/
│       ├── __init__.py                 # (✅ Implemented)
│       ├── helpers.py                  # Utility functions (TO BE IMPLEMENTED)
│       └── constants.py                # Constants & enums (TO BE IMPLEMENTED)
│
├── docs/
│   └── TRANSACTION_ENGINE.md           # Transaction engine docs (✅ Implemented)
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
│   ├── __init__.py                     # (✅ Implemented)
│   ├── test_transaction_engine.py      # Transaction engine tests (✅ Implemented)
│   ├── test_bot.py                     # (TO BE IMPLEMENTED)
│   ├── test_strategies.py              # (TO BE IMPLEMENTED)
│   └── test_oracle.py                  # (TO BE IMPLEMENTED)
│
├── scripts/
│   ├── run_transaction_engine.py       # Run transaction engine (✅ Implemented)
│   ├── install.sh                      # Linux/Mac installation (TO BE IMPLEMENTED)
│   ├── install.bat                     # Windows installation (TO BE IMPLEMENTED)
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
