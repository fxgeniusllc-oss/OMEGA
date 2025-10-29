# OMEGA DeFi Trading Bot - Technical Documentation

## Overview

The OMEGA DeFi Trading Bot is a sophisticated multi-chain arbitrage system that monitors prices across decentralized exchanges (DEXs), bridges, and centralized exchanges (CEXs) to identify and execute profitable trading opportunities.

## Features

### Multi-Chain Support
- **Polygon** (default enabled)
- **Ethereum**
- **Arbitrum**
- **Optimism**
- **Base**
- **BSC**
- **Solana** (partial support)

### Supported DEXs (13 integrations)
1. QuickSwap
2. Uniswap V3
3. SushiSwap
4. Balancer V2
5. Curve
6. Paraswap
7. 1inch
8. DODO
9. KyberDMM
10. Synapse
11. Firebird
12. 0x Protocol
13. Odos

### Supported Bridge Protocols
1. Stargate (0.06% fee)
2. Across (0.05% fee)
3. Connext (0.04% fee)
4. Hop Protocol (0.05% fee)
5. Synapse (0.03% fee)

### Trading Strategies

1. **Cross-Chain Arbitrage** - Buy on one chain, sell on another
2. **Bridge Arbitrage** - Exploit price differences across bridge protocols
3. **Mempool Watching** - Front-run profitable transactions (planned)
4. **Market Making** - Provide liquidity and capture spreads (planned)
5. **Statistical Arbitrage** - Use statistical models (planned)
6. **Gamma Scalping** - Options-based strategies (planned)
7. **Funding Rate Arbitrage** - Exploit perpetual funding rates (planned)
8. **Volatility Arbitrage** - Trade volatility differences (planned)

## Architecture

### Core Components

#### 1. PriceOracle
Central system for USD price conversion and normalization.
```python
oracle = PriceOracle()
price = await oracle.get_usd_price("WETH")  # Returns Decimal
usd_value = await oracle.convert_to_usd(Decimal("10"), "WETH")
```

#### 2. PriceMonitor
Tracks prices across all sources and maintains historical data.
```python
monitor = PriceMonitor(oracle)
monitor.add_price(price_data)
monitor.log_price_comparison("polygon", "WETH", "USDC")
```

#### 3. BlockchainInterface
Handles all blockchain interactions across multiple chains.
```python
blockchain = BlockchainInterface(config, oracle)
gas_price = await blockchain.get_gas_price_usd("polygon")
tx_hash = await blockchain.send_transaction(tx_data, "polygon")
```

#### 4. CrossChainArbitrageur
Executes cross-chain arbitrage strategies.
```python
arb = CrossChainArbitrageur(blockchain, monitor, oracle, config)
opportunity = await arb.find_cross_chain_opportunity()
result = await arb.execute_cross_chain_swap(opportunity)
```

#### 5. BridgeArbitrageur
Executes bridge protocol arbitrage.
```python
bridge = BridgeArbitrageur(blockchain, monitor, oracle, config)
opportunity = await bridge.find_bridge_opportunity()
```

#### 6. UnifiedTradingBot
Main orchestrator that coordinates all strategies.
```python
bot = UnifiedTradingBot(config)
await bot.run()
```

## Configuration

### Environment Variables

All configuration is done via environment variables (`.env` file):

#### Trading Mode
```bash
MODE=DEV                    # LIVE, DEV, or SIM
AUTO_START_ARBITRAGE=true   # Auto-execute trades
```

#### Blockchain Settings
```bash
BOT_ADDRESS=0x...
EXECUTOR_ADDRESS=0x...
PRIVATE_KEY=0x...
```

#### RPC Configuration
```bash
INFURA_POLYGON_RPC=https://...
QUICKNODE_RPC_URL=https://...
ALCHEMY_RPC_URL=https://...
```

#### Chain Enablement
```bash
POLYGON_ENABLED=true
ETHEREUM_ENABLED=false
ARBITRUM_ENABLED=false
```

#### DEX Configuration
```bash
ACTIVE_DEXS=quickswap,uniswap_v3,sushiswap,balancer,curve
QUICKSWAP_ROUTER=0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff
UNISWAP_V3_ROUTER=0xE592427A0AEce92De3Edee1F18E0157C05861564
```

#### Strategy Configuration
```bash
ACTIVE_STRATEGIES=CROSS_CHAIN_ARBITRAGE,BRIDGE_ARBITRAGE
FLASHLOAN_PROVIDER=BALANCER_VAULT
```

#### Risk Management
```bash
MIN_PROFIT_USD=15           # Minimum profit to execute
MIN_LIQUIDITY_USD=50000     # Minimum pool liquidity
MAX_TRADE_SIZE_USD=2000000  # Maximum trade size
SLIPPAGE_BPS=50            # 0.5% slippage tolerance
GAS_PRICE_MULTIPLIER=1.2   # 20% gas price buffer
```

## Data Models

### PriceData
```python
@dataclass
class PriceData:
    source: str              # DEX/Bridge/CEX name
    chain: str              # Blockchain name
    token_a: str            # First token symbol
    token_b: str            # Second token symbol
    price_usd: Decimal      # Price in USD
    token_a_usd: Decimal    # Token A price in USD
    token_b_usd: Decimal    # Token B price in USD
    timestamp: datetime     # When price was fetched
    liquidity_usd: Decimal  # Pool liquidity in USD
    fee_percent: Decimal    # Trading fee percentage
    source_type: str        # "DEX", "BRIDGE", or "CEX"
```

### TradingOpportunity
```python
@dataclass
class TradingOpportunity:
    strategy: TradingStrategy
    token_a: str
    token_b: str
    amount_usd: Decimal
    expected_profit_usd: Decimal
    profit_percentage: float
    confidence: float
    buy_price_usd: Decimal
    sell_price_usd: Decimal
    timestamp: datetime
    price_sources: List[PriceData]
```

### ExecutionResult
```python
@dataclass
class ExecutionResult:
    success: bool
    tx_hash: Optional[str]
    block_number: Optional[int]
    gas_used: Optional[int]
    actual_profit_usd: Decimal
    entry_price_usd: Decimal
    exit_price_usd: Decimal
    slippage_percent: float
    execution_time: float
    timestamp: datetime
    error_message: Optional[str]
```

## Execution Flow

### Cross-Chain Arbitrage

1. **Scan Phase**
   - Fetch prices from all enabled DEXs across all enabled chains
   - Normalize all prices to USD using PriceOracle
   - Store prices in PriceMonitor

2. **Analysis Phase**
   - Compare prices across all sources
   - Calculate potential profit considering:
     - Entry/exit prices
     - Trading fees
     - Gas costs
     - Bridge fees (if applicable)
     - Flash loan fees
     - Slippage

3. **Opportunity Detection**
   - Identify buy-low/sell-high pairs
   - Verify liquidity sufficiency
   - Check profit threshold (MIN_PROFIT_USD)
   - Calculate confidence score

4. **Execution Phase**
   ```
   Step 1: Initiate flash loan
   Step 2: Execute buy order on source DEX
   Step 3: Bridge tokens to destination chain (if needed)
   Step 4: Execute sell order on destination DEX
   Step 5: Repay flash loan + fees
   Step 6: Calculate net profit
   ```

5. **Results Logging**
   - Transaction hash
   - Block number
   - Gas used
   - Actual profit/loss
   - Execution time
   - ROI percentage

## Logging System

### Colored Console Output
- **DEBUG** - Cyan
- **INFO** - Light Green
- **WARNING** - Yellow
- **ERROR** - Light Red
- **CRITICAL** - Magenta
- **TX** - Blue (transaction hashes)
- **PROFIT** - Light Green
- **LOSS** - Light Red

### Log Levels
```python
logger.debug("Detailed debug information")
logger.info("General information")
logger.warning("Warning messages")
logger.error("Error messages")
logger.critical("Critical failures")
```

### Log Files
- **trading_bot.log** - Main application log
- **trades_history.json** - Trade execution history (planned)

## Running the Bot

### Quick Start (Linux/Mac)
```bash
# Install
bash scripts/install.sh

# Configure
nano .env

# Run
bash scripts/run.sh
```

### Quick Start (Windows)
```batch
REM Install
scripts\install.bat

REM Configure
notepad .env

REM Run
scripts\run.bat
```

### Docker
```bash
# Build and run
cd docker
docker-compose up -d

# View logs
docker-compose logs -f bot

# Stop
docker-compose down
```

### Manual Run
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate.bat  # Windows

# Install dependencies
pip install -r requirements.txt

# Run bot
python -m src.bot
```

## Testing

### Run Tests
```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_bot.py

# Run with verbose output
pytest -v
```

### Test Structure
```
tests/
├── __init__.py
├── test_bot.py          # Core bot tests
├── test_strategies.py   # Strategy tests (planned)
└── test_oracle.py       # Price oracle tests (planned)
```

## Security Considerations

### Private Key Management
- **NEVER** commit `.env` file to git
- Use hardware wallets in production
- Consider key management services (AWS KMS, HashiCorp Vault)
- Rotate keys regularly

### RPC Security
- Use authenticated RPC endpoints
- Implement rate limiting
- Have backup RPC providers
- Monitor RPC usage

### Smart Contract Security
- Audit all contract interactions
- Use established DEX routers only
- Implement transaction simulation before execution
- Set reasonable gas limits

### Risk Management
- Start with small trade sizes
- Test thoroughly in SIM/DEV modes
- Monitor gas prices
- Implement stop-loss mechanisms
- Set profit-taking thresholds

## Performance Optimization

### RPC Optimization
- Use WebSocket connections for real-time data
- Implement connection pooling
- Cache frequently accessed data
- Use local/private nodes for production

### Price Fetching
- Parallel price fetching across sources
- Implement caching with TTL
- Use GraphQL where available
- Batch requests when possible

### Execution Optimization
- Pre-approve tokens to save gas
- Use gas estimation before execution
- Implement transaction queuing
- Use flashbots for MEV protection

## Monitoring & Alerts

### Metrics to Monitor
- Total trades executed
- Success/failure rate
- Average profit per trade
- Gas costs
- Execution time
- RPC latency

### Alert Conditions
- Failed trades
- Low balance
- RPC failures
- Unusual gas prices
- Large slippage

### Integration Options
- Telegram notifications
- Email alerts
- Webhook notifications
- Discord integration
- Slack integration

## Troubleshooting

### Common Issues

#### Import Errors
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

#### RPC Connection Errors
```bash
# Solution: Check RPC URLs in .env
# Verify network connectivity
# Try backup RPC providers
```

#### Insufficient Funds
```bash
# Solution: Fund wallet with native tokens
# Check token allowances
# Verify gas price settings
```

#### No Opportunities Found
```bash
# Solution: Lower MIN_PROFIT_USD threshold
# Enable more DEXs in ACTIVE_DEXS
# Enable more chains
# Adjust SLIPPAGE_BPS
```

## Development

### Adding a New DEX

1. Add router address to `.env`:
```bash
NEWDEX_ROUTER=0x...
```

2. Update `load_dex_routers()` in `bot.py`:
```python
def load_dex_routers() -> Dict[str, str]:
    return {
        # ... existing DEXs ...
        "newdex": os.getenv("NEWDEX_ROUTER", "0x..."),
    }
```

3. Add to `ACTIVE_DEXS`:
```bash
ACTIVE_DEXS=quickswap,uniswap_v3,newdex
```

### Adding a New Chain

1. Add RPC URLs to `.env`:
```bash
NEWCHAIN_RPC_URL=https://...
NEWCHAIN_RPC_WS=wss://...
NEWCHAIN_ENABLED=true
```

2. Update `load_rpc_urls()` in `bot.py`:
```python
def load_rpc_urls() -> Dict[str, Dict[str, str]]:
    return {
        # ... existing chains ...
        "newchain": {
            "http": os.getenv("NEWCHAIN_RPC_URL"),
            "ws": os.getenv("NEWCHAIN_RPC_WS"),
        },
    }
```

3. Update `load_config()` to check enablement:
```python
if os.getenv("NEWCHAIN_ENABLED", "false").lower() == "true":
    enabled_chains.append("newchain")
```

## API Reference

### PriceOracle

```python
class PriceOracle:
    async def get_usd_price(self, token: str) -> Decimal
    async def convert_to_usd(self, amount: Decimal, token: str) -> Decimal
    async def convert_from_usd(self, usd_amount: Decimal, token: str) -> Decimal
```

### BlockchainInterface

```python
class BlockchainInterface:
    async def get_gas_price_usd(self, chain: str = "polygon") -> Decimal
    async def send_transaction(self, tx_data: Dict, chain: str) -> str
```

### CrossChainArbitrageur

```python
class CrossChainArbitrageur:
    async def fetch_all_dex_prices(self, token_a: str, token_b: str) -> List[PriceData]
    async def find_cross_chain_opportunity(self) -> Optional[TradingOpportunity]
    async def execute_cross_chain_swap(self, opp: TradingOpportunity) -> ExecutionResult
```

### UnifiedTradingBot

```python
class UnifiedTradingBot:
    async def run(self) -> None
```

## License

This project is proprietary software owned by FX Genius LLC.

## Support

For issues, questions, or contributions, please contact the development team.

## Version History

- **v1.0.0** (Current)
  - Initial release
  - Multi-chain support (Polygon, Ethereum, Arbitrum, Optimism, Base, BSC)
  - 13 DEX integrations
  - 5 bridge protocol integrations
  - Cross-chain arbitrage strategy
  - Bridge arbitrage strategy
  - USD-normalized pricing
  - Comprehensive logging
  - Docker support
  - Cross-platform scripts

## Roadmap

- [ ] Mempool watching strategy implementation
- [ ] CEX integration (Binance, Coinbase, Kraken)
- [ ] Real-time price feeds via WebSocket
- [ ] Machine learning price prediction
- [ ] Advanced risk management
- [ ] Multi-hop arbitrage routes
- [ ] Gas optimization strategies
- [ ] MEV protection via Flashbots
- [ ] Telegram bot interface
- [ ] Web dashboard
- [ ] Backtesting framework
- [ ] Performance analytics
- [ ] Automated tax reporting
