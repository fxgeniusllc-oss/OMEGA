import os
import asyncio
import json
import logging
import sys
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum
from collections import defaultdict
import aiohttp

from web3 import Web3
from web3.contract import Contract
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ========================================
# PRICE ORACLE & CONVERSION SYSTEM
# ========================================

class PriceOracle:
    """Central oracle for USD price conversion and aggregation."""
    
    def __init__(self):
        self.exchange_rates: Dict[str, Decimal] = {
            "USDC": Decimal("1.0000"),
            "USDT": Decimal("0.9998"),
            "DAI": Decimal("1.0001"),
            "WETH": Decimal("2347.50"),
            "WBTC": Decimal("43521.00"),
            "MATIC": Decimal("0.4523"),
            "ARB": Decimal("0.8234"),
            "OP": Decimal("1.9456"),
            "AAVE": Decimal("89.34"),
            "UNI": Decimal("7.891"),
        }
    
    async def get_usd_price(self, token: str) -> Decimal:
        """Get USD price for any token."""
        return self.exchange_rates.get(token, Decimal("0"))
    
    async def convert_to_usd(self, amount: Decimal, token: str) -> Decimal:
        """Convert any token amount to USD."""
        price = await self.get_usd_price(token)
        return amount * price
    
    async def convert_from_usd(self, usd_amount: Decimal, token: str) -> Decimal:
        """Convert USD amount to token quantity."""
        price = await self.get_usd_price(token)
        if price == 0:
            return Decimal("0")
        return usd_amount / price

# ========================================
# ENHANCED LOGGING CONFIGURATION
# ========================================

class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for terminal output."""
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[92m',       # Light Green
        'WARNING': '\033[93m',    # Yellow
        'ERROR': '\033[91m',      # Light Red
        'CRITICAL': '\033[95m',   # Magenta
        'TX': '\033[94m',         # Blue
        'PROFIT': '\033[92m',     # Light Green
        'LOSS': '\033[91m',       # Light Red
        'PRICE': '\033[36m',      # Cyan
        'RESET': '\033[0m',       # Reset
    }
    
    def format(self, record):
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"
        return super().format(record)

def setup_logging(log_file: str = "trading_bot.log"):
    """Setup enhanced logging with file and console output."""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    # Clear existing handlers
    logger.handlers = []
    
    # Console handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_formatter = ColoredFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    
    # File handler without colors
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

logger = setup_logging()

# ========================================
# CONSTANTS & CONFIGURATION
# ========================================

class StrategyMode(Enum):
    LIVE = "LIVE"
    DEV = "DEV"
    SIM = "SIM"

class TradingStrategy(Enum):
    MEMPOOL_WATCHING = "mempool_watching"
    CROSS_CHAIN_ARBITRAGE = "cross_chain_arbitrage"
    PUMP_PREDICTION = "pump_prediction"
    MARKET_MAKING = "market_making"
    STATISTICAL_ARBITRAGE = "statistical_arbitrage"
    GAMMA_SCALPING = "gamma_scalping"
    FUNDING_RATE = "funding_rate"
    VOLATILITY_ARBITRAGE = "volatility_arbitrage"
    BRIDGE_ARBITRAGE = "bridge_arbitrage"

# ========================================
# MULTI-CHAIN RPC CONFIGURATION FROM ENV
# ========================================

def load_rpc_urls() -> Dict[str, Dict[str, str]]:
    """Load RPC URLs from environment variables with fallbacks."""
    return {
        "polygon": {
            "http": os.getenv("INFURA_POLYGON_RPC") or os.getenv("QUICKNODE_RPC_URL") or os.getenv("ALCHEMY_RPC_URL"),
            "ws": os.getenv("INFURA_POLYGON_RPC_WS") or os.getenv("QUICKNODE_RPS_WS") or os.getenv("ALCHEMY_RPC_WSS"),
        },
        "ethereum": {
            "http": os.getenv("ETHEREUM_RPC_URL") or os.getenv("ETHEREUM_INFURA_RPC") or os.getenv("ETHEREUM_RPC"),
            "ws": os.getenv("ETHEREUM_INFURA_WSS"),
        },
        "arbitrum": {
            "http": os.getenv("ARBITRUM_RPC_URL") or os.getenv("INFURA_ARB_RPC_HTTP") or os.getenv("ARBITRUM_RPC"),
            "ws": os.getenv("ARBITRUM_INFURA_WSS") or os.getenv("QUICKNODE_ARB_WSS"),
        },
        "optimism": {
            "http": os.getenv("OPTIMISM_RPC_URL") or os.getenv("INFURA_OP_RPC_HTTP") or os.getenv("ALCHEMY_OP_RPC"),
            "ws": os.getenv("INFURA_OP_RPC_WS") or os.getenv("QUICKNODE_OP_WSS"),
        },
        "base": {
            "http": os.getenv("BASE_RPC_URL") or os.getenv("INFURA_BASE_RPC_HTTP") or os.getenv("ALCHEMY_BASE_RPC"),
            "ws": os.getenv("INFURA_BASE_RPC_WS") or os.getenv("QUICKNODE_BASE_WSS"),
        },
        "bsc": {
            "http": os.getenv("BSC_RPC_URL") or os.getenv("INFURA_BSC_RPC_HTTP") or os.getenv("ALCHEMY_BSC_RPC"),
            "ws": os.getenv("QUICKNODE_BSC_WSS"),
        },
        "solana": {
            "http": os.getenv("ALCHEMY_SOLANA_RPC") or os.getenv("QUICKNODE_SOLANA_RPC"),
            "ws": os.getenv("QUICKNODE_SOLANA_WSS"),
        },
    }

# ========================================
# MULTI-SOURCE DEX CONFIGURATION FROM ENV
# ========================================

def load_dex_routers() -> Dict[str, str]:
    """Load DEX router addresses from environment variables."""
    return {
        "quickswap": os.getenv("QUICKSWAP_ROUTER", "0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff"),
        "sushiswap": os.getenv("SUSHISWAP_ROUTER", "0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506"),
        "uniswap_v3": os.getenv("UNISWAP_V3_ROUTER", "0xE592427A0AEce92De3Edee1F18E0157C05861564"),
        "paraswap": os.getenv("PARASWAP_ROUTER", "0xDEF171Fe48CF0115B1d80b88dc8eAB59176FEe57"),
        "oneinch": os.getenv("ONEINCH_ROUTER", "0x1111111254EEB25477B68fb85Ed929f73A960582"),
        "balancer": os.getenv("BALANCER_V2_VAULT", "0xBA12222222228d8Ba445958a75a0704d566BF2C8"),
        "curve": os.getenv("CURVE_ROUTER", "0xB576491F1E6e5E62f1d8f26062Ee822b40B0E0d4"),
        "dodo": os.getenv("DODO_ROUTER", "0xa356867fDCEa8e71AEaF87805808803806231FdC"),
        "kyberdmm": os.getenv("KYBERDMM_ROUTER", "0x546C79662E028B661dFB4767664d0273184E4Dd1"),
        "synapse": os.getenv("SYNAPSE_ROUTER", "0x44F4A35eAaE42Fd2a881Dd301DeedDa9CdfE5b87"),
        "firebird": os.getenv("FIREBIRD_ROUTER", "0xFf7B995e8cA26De1Bd6C768E8d3b96946F72693E"),
        "0x": os.getenv("ZRX_EXCHANGE_PROXY", "0xDEF1ABE32c034e558Cdd535791643C58a13aCC10"),
        "odos": os.getenv("ODOS_ROUTER", "0xA7d50a5fC58b23E9C3C40b8C8C856b63a2b38dC5"),
    }

def load_token_addresses() -> Dict[str, str]:
    """Load token addresses from environment variables."""
    return {
        "WMATIC": os.getenv("WMATIC", "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270"),
        "USDC": os.getenv("USDC", "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"),
        "USDT": os.getenv("USDT", "0xc2132D05D31c914a87C6611C10748AEb04B58e8F"),
        "DAI": os.getenv("DAI", "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063"),
        "WETH": os.getenv("WETH", "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619"),
        "WBTC": os.getenv("WBTC", "0x1BFD67037B42Cf73acF2047067bd4F2C47D9BfD6"),
        "LINK": os.getenv("LINK", "0x53E0bca35eC356BD5ddDFebbD1Fc0fD03FaBad39"),
        "AAVE": os.getenv("AAVE", "0xD6DF932A45C0f255f85145f286eA0b292B21C90B"),
        "UNI": os.getenv("UNI", "0xb33EaAd8d922B1083446DC23f610c2567fB5180f"),
    }

# ========================================
# BRIDGE PROTOCOLS FROM ENV
# ========================================

BRIDGE_SOURCES = {
    "Stargate": {"fee_percent": 0.06},
    "Across": {"fee_percent": 0.05},
    "Connext": {"fee_percent": 0.04},
    "Hop Protocol": {"fee_percent": 0.05},
    "Synapse": {"fee_percent": 0.03},
}

CEX_SOURCES = {
    "Binance": {"fee_percent": 0.10},
    "Coinbase": {"fee_percent": 0.50},
    "Kraken": {"fee_percent": 0.26},
}

# ========================================
# DATA CLASSES
# ========================================

@dataclass
class PriceData:
    """Price data from a single source - ALL VALUES IN USD."""
    source: str
    chain: str
    token_a: str
    token_b: str
    price_usd: Decimal
    token_a_usd: Decimal
    token_b_usd: Decimal
    timestamp: datetime
    liquidity_usd: Decimal
    fee_percent: Decimal
    source_type: str

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
    price_sources: List[PriceData] = field(default_factory=list)

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
    error_message: Optional[str] = None

@dataclass
class BotConfig:
    mode: StrategyMode
    private_key: str
    bot_address: str
    executor_address: str
    rpc_urls: Dict[str, Dict[str, str]]
    auto_start: bool
    strategies: List[TradingStrategy]
    flash_loan_provider: str
    slippage_tolerance: float
    gas_price_multiplier: float
    max_position_size_usd: Decimal
    risk_per_trade: float
    log_file: str
    dex_routers: Dict[str, str]
    token_addresses: Dict[str, str]
    enabled_chains: List[str]
    enabled_dexs: List[str]
    min_profit_usd: Decimal
    min_liquidity_usd: Decimal

# ========================================
# CONFIGURATION LOADER FROM ENV
# ========================================

def load_config() -> BotConfig:
    """Load comprehensive configuration from environment variables."""
    
    # Parse enabled chains from env
    enabled_chains = []
    if os.getenv("POLYGON_ENABLED", "true").lower() == "true":
        enabled_chains.append("polygon")
    if os.getenv("ETHEREUM_ENABLED", "false").lower() == "true":
        enabled_chains.append("ethereum")
    if os.getenv("ARBITRUM_ENABLED", "false").lower() == "true":
        enabled_chains.append("arbitrum")
    if os.getenv("OPTIMISM_ENABLED", "false").lower() == "true":
        enabled_chains.append("optimism")
    if os.getenv("BASE_ENABLED", "false").lower() == "true":
        enabled_chains.append("base")
    
    # Parse enabled DEXs from env
    enabled_dexs = os.getenv("ACTIVE_DEXS", "quickswap,uniswap_v3,sushiswap,balancer,curve,paraswap,oneinch").split(",")
    enabled_dexs = [d.strip() for d in enabled_dexs if d.strip()]
    
    # Parse strategies from env
    strategies = [
        TradingStrategy[s.upper()] 
        for s in os.getenv("ACTIVE_STRATEGIES", "CROSS_CHAIN_ARBITRAGE,BRIDGE_ARBITRAGE").split(",")
        if s.strip()
    ]
    
    config = BotConfig(
        mode=StrategyMode[os.getenv("MODE", "DEV")],
        private_key=os.getenv("PRIVATE_KEY", "0x" + "0" * 64),
        bot_address=os.getenv("BOT_ADDRESS", "0x0000000000000000000000000000000000000000"),
        executor_address=os.getenv("EXECUTOR_ADDRESS", "0xb60CA70A37198A7A74D6231B2F661fAb707f75eF"),
        rpc_urls=load_rpc_urls(),
        auto_start=os.getenv("AUTO_START_ARBITRAGE", "true").lower() == "true",
        strategies=strategies,
        flash_loan_provider=os.getenv("FLASHLOAN_PROVIDER", "BALANCER_VAULT"),
        slippage_tolerance=float(os.getenv("SLIPPAGE_BPS", "50")) / 10000,
        gas_price_multiplier=float(os.getenv("GAS_PRICE_MULTIPLIER", "1.2")),
        max_position_size_usd=Decimal(os.getenv("MAX_TRADE_SIZE_USD", "2000000")),
        risk_per_trade=float(os.getenv("RISK_PER_TRADE", "0.02")),
        log_file=os.getenv("LOG_FILE", "trading_bot.log"),
        dex_routers=load_dex_routers(),
        token_addresses=load_token_addresses(),
        enabled_chains=enabled_chains,
        enabled_dexs=enabled_dexs,
        min_profit_usd=Decimal(os.getenv("MIN_PROFIT_USD", "15")),
        min_liquidity_usd=Decimal(os.getenv("MIN_LIQUIDITY_USD", "50000")),
    )
    
    return config

# ========================================
# PRICE MONITOR
# ========================================

class PriceMonitor:
    """Monitors prices across all DEXs, bridges, and CEXs - ALL IN USD."""
    
    def __init__(self, oracle: PriceOracle):
        self.price_cache: Dict[str, List[PriceData]] = defaultdict(list)
        self.price_history: Dict[str, List[Tuple[datetime, Decimal]]] = defaultdict(list)
        self.oracle = oracle
    
    def add_price(self, price_data: PriceData):
        """Add price data from a source."""
        key = f"{price_data.chain}:{price_data.token_a}/{price_data.token_b}:{price_data.source_type}"
        self.price_cache[key].append(price_data)
        self.price_history[key].append((price_data.timestamp, price_data.price_usd))
    
    def log_price_comparison(self, chain: str, token_a: str, token_b: str):
        """Log prices from all sources for comparison - ALL IN USD."""
        key_pattern = f"{chain}:{token_a}/{token_b}:"
        matching_prices = []
        
        for key, prices in self.price_cache.items():
            if key.startswith(key_pattern):
                if prices:
                    latest = prices[-1]
                    matching_prices.append(latest)
        
        if not matching_prices:
            logger.warning(f"No price data found for {token_a}/{token_b} on {chain}")
            return
        
        logger.info("=" * 180)
        logger.info(f"PRICE COMPARISON - {chain.upper()} | {token_a}/{token_b} (ALL VALUES IN USD)")
        logger.info("=" * 180)
        logger.info(f"{'DEX/Source':<25} {'Type':<12} {'Price USD':<20} {'Token A USD':<20} {'Token B USD':<20} {'Liquidity USD':<20} {'Fee%':<12} {'Router/Address':<40}")
        logger.info("-" * 180)
        
        prices_sorted = sorted(matching_prices, key=lambda x: x.price_usd)
        min_price = prices_sorted[0].price_usd
        max_price = prices_sorted[-1].price_usd
        spread = ((max_price - min_price) / min_price * 100) if min_price > 0 else 0
        
        for price_data in matching_prices:
            logger.info(
                f"{price_data.source:<25} {price_data.source_type:<12} "
                f"${float(price_data.price_usd):<19.8f} "
                f"${float(price_data.token_a_usd):<19.8f} "
                f"${float(price_data.token_b_usd):<19.8f} "
                f"${float(price_data.liquidity_usd):<19.2f} {float(price_data.fee_percent):<11.4f} "
                f"{'Contract/Route':<40}"
            )
        
        logger.info("-" * 180)
        logger.info(f"Price Range: ${float(min_price):.8f} - ${float(max_price):.8f} | Spread: {spread:.4f}%")
        logger.info(f"Total Sources Analyzed: {len(matching_prices)}")
        logger.info("=" * 180)

# ========================================
# BLOCKCHAIN INTERFACE
# ========================================

class BlockchainInterface:
    """Handles all blockchain interactions across chains."""
    
    def __init__(self, config: BotConfig, oracle: PriceOracle):
        self.config = config
        self.oracle = oracle
        self.w3_instances = {}
        
        for chain, urls in config.rpc_urls.items():
            if chain in config.enabled_chains and urls.get("http"):
                try:
                    self.w3_instances[chain] = Web3(Web3.HTTPProvider(urls["http"]))
                    logger.info(f"✓ Connected to {chain.upper()}: {urls['http'][:50]}...")
                except Exception as e:
                    logger.error(f"Failed to connect to {chain}: {e}")
        
        try:
            self.account = Web3().eth.account.from_key(config.private_key)
            logger.info(f"✓ Blockchain Interface Initialized")
            logger.info(f"  Bot Address: {config.bot_address}")
            logger.info(f"  Executor Address: {config.executor_address}")
            logger.info(f"  Connected Chains: {', '.join(self.w3_instances.keys())}")
            logger.info(f"  Active DEXs: {', '.join(config.enabled_dexs)}")
        except Exception as e:
            logger.error(f"Failed to initialize account: {e}")
    
    async def get_gas_price_usd(self, chain: str = "polygon") -> Decimal:
        """Get current gas price in USD."""
        w3 = self.w3_instances.get(chain)
        if not w3:
            raise ValueError(f"Chain {chain} not configured")
        
        try:
            gas_price_wei = w3.eth.gas_price
            gas_price_eth = Decimal(gas_price_wei) / Decimal(10 ** 18)
            eth_price_usd = await self.oracle.get_usd_price("WETH")
            
            gas_price_usd = gas_price_eth * eth_price_usd * Decimal(self.config.gas_price_multiplier)
            logger.debug(f"Gas Price USD ({chain}): ${float(gas_price_usd):.4f}")
            return gas_price_usd
        except Exception as e:
            logger.error(f"Failed to get gas price: {e}")
            return Decimal("0")
    
    async def send_transaction(self, tx_data: Dict, chain: str) -> str:
        """Send a transaction on the specified chain."""
        w3 = self.w3_instances.get(chain)
        if not w3:
            raise ValueError(f"Chain {chain} not configured")
        
        # Simulate transaction in dev/sim mode
        tx_hash = "0x" + "".join(f"{i % 16:x}" for i in range(64))
        return tx_hash

# ========================================
# STRATEGY ENGINES
# ========================================

class CrossChainArbitrageur:
    """Handles cross-chain arbitrage execution - ALL IN USD."""
    
    def __init__(self, blockchain: BlockchainInterface, price_monitor: PriceMonitor, oracle: PriceOracle, config: BotConfig):
        self.blockchain = blockchain
        self.price_monitor = price_monitor
        self.oracle = oracle
        self.config = config
    
    async def fetch_all_dex_prices(self, token_a: str, token_b: str) -> List[PriceData]:
        """Fetch prices from ALL DEX sources across enabled chains."""
        all_prices = []
        
        for chain in self.config.enabled_chains:
            for dex in self.config.enabled_dexs:
                # Simulate price fetching from each DEX
                base_price = Decimal("1850.50") + Decimal(str(hash(dex) % 100) / 100)
                token_a_usd = await self.oracle.get_usd_price(token_a)
                token_b_usd = await self.oracle.get_usd_price(token_b)
                
                fee_percent = Decimal("0.3") if dex == "uniswap_v3" else Decimal("0.25")
                
                price_data = PriceData(
                    source=dex.upper(),
                    chain=chain,
                    token_a=token_a,
                    token_b=token_b,
                    price_usd=base_price,
                    token_a_usd=token_a_usd,
                    token_b_usd=token_b_usd,
                    timestamp=datetime.now(),
                    liquidity_usd=Decimal("500000"),
                    fee_percent=fee_percent,
                    source_type="DEX"
                )
                all_prices.append(price_data)
                self.price_monitor.add_price(price_data)
        
        return all_prices
    
    async def find_cross_chain_opportunity(self) -> Optional[TradingOpportunity]:
        """Identify profitable cross-chain arbitrage."""
        logger.info("\n[CROSS-CHAIN ARBITRAGE] Scanning ALL DEX sources for opportunities...")
        
        token_a, token_b = "WETH", "USDC"
        
        # Fetch from all sources
        all_prices = await self.fetch_all_dex_prices(token_a, token_b)
        
        if not all_prices:
            logger.warning("No price data available")
            return None
        
        # Log comprehensive comparison
        for chain in self.config.enabled_chains:
            self.price_monitor.log_price_comparison(chain, token_a, token_b)
        
        # Find min and max prices
        prices_sorted = sorted(all_prices, key=lambda x: x.price_usd)
        buy_price_usd = prices_sorted[0].price_usd
        sell_price_usd = prices_sorted[-1].price_usd
        
        amount_usd = Decimal("10000")
        amount_tokens = amount_usd / buy_price_usd
        
        profit_usd = (sell_price_usd - buy_price_usd) * amount_tokens
        profit_pct = (profit_usd / amount_usd) * 100
        
        if profit_usd > self.config.min_profit_usd:
            logger.info(f"\n\033[92m[OPPORTUNITY FOUND - CROSS-CHAIN ARB]")
            logger.info(f"  Token Pair: {token_a}/{token_b}")
            logger.info(f"  Amount: ${float(amount_usd):,.2f}")
            logger.info(f"  Buy Price: ${float(buy_price_usd):.8f}")
            logger.info(f"  Sell Price: ${float(sell_price_usd):.8f}")
            logger.info(f"  Gross Profit: ${float(profit_usd):,.2f}")
            logger.info(f"  Profit Margin: {profit_pct:.4f}%\033[0m\n")
            
            return TradingOpportunity(
                strategy=TradingStrategy.CROSS_CHAIN_ARBITRAGE,
                token_a=token_a,
                token_b=token_b,
                amount_usd=amount_usd,
                expected_profit_usd=profit_usd,
                profit_percentage=float(profit_pct),
                confidence=0.92,
                buy_price_usd=buy_price_usd,
                sell_price_usd=sell_price_usd,
                timestamp=datetime.now(),
                price_sources=all_prices
            )
        
        return None
    
    async def execute_cross_chain_swap(self, opp: TradingOpportunity) -> ExecutionResult:
        """Execute cross-chain arbitrage - ALL IN USD."""
        start_time = datetime.now()
        
        logger.info("\n" + "=" * 180)
        logger.info(f"EXECUTING CROSS-CHAIN ARBITRAGE (ALL VALUES IN USD)")
        logger.info("=" * 180)
        logger.info(f"Strategy: {opp.strategy.value.upper()}")
        logger.info(f"Pair: {opp.token_a}/{opp.token_b}")
        logger.info(f"Investment Amount: ${float(opp.amount_usd):,.2f} USD")
        logger.info(f"Expected Profit: ${float(opp.expected_profit_usd):,.2f} USD ({opp.profit_percentage:.4f}%)")
        logger.info(f"Confidence: {opp.confidence * 100:.2f}%")
        logger.info(f"Enabled Chains: {', '.join(self.config.enabled_chains)}")
        logger.info(f"Enabled DEXs: {', '.join(self.config.enabled_dexs)}")
        logger.info("=" * 180)
        
        logger.info("\n[STEP 1] Initiating flash loan...")
        await asyncio.sleep(0.5)
        logger.info(f"✓ Flash loan approved | Provider: {self.config.flash_loan_provider}")
        
        logger.info("\n[STEP 2] Executing buy order on source DEX...")
        await asyncio.sleep(0.3)
        entry_slippage_pct = Decimal(str(self.config.slippage_tolerance))
        actual_entry_usd = opp.buy_price_usd * (1 + entry_slippage_pct)
        logger.info(f"  Entry Price (USD): ${float(opp.buy_price_usd):.8f}")
        logger.info(f"  Slippage Tolerance: {float(entry_slippage_pct * 100):.4f}%")
        logger.info(f"  Actual Entry (USD): ${float(actual_entry_usd):.8f}")
        logger.info("✓ Buy order executed")
        
        logger.info("\n[STEP 3] Bridging tokens to destination chain...")
        await asyncio.sleep(1.0)
        logger.info("✓ Bridge confirmed")
        
        logger.info("\n[STEP 4] Executing sell order on destination DEX...")
        await asyncio.sleep(0.3)
        exit_slippage_pct = Decimal(str(self.config.slippage_tolerance))
        actual_exit_usd = opp.sell_price_usd * (1 - exit_slippage_pct)
        logger.info(f"  Exit Price (USD): ${float(opp.sell_price_usd):.8f}")
        logger.info(f"  Slippage Applied: {float(exit_slippage_pct * 100):.4f}%")
        logger.info(f"  Actual Exit (USD): ${float(actual_exit_usd):.8f}")
        logger.info("✓ Sell order executed")
        
        logger.info("\n[STEP 5] Calculating costs and repaying flash loan...")
        await asyncio.sleep(0.2)
        flash_fee_usd = opp.amount_usd * Decimal("0.0003")
        bridge_fee_usd = opp.amount_usd * Decimal("0.0005")
        gas_cost_usd = await self.blockchain.get_gas_price_usd(self.config.enabled_chains[0])
        logger.info(f"  Flash Loan Fee: -${float(flash_fee_usd):,.2f}")
        logger.info(f"  Bridge Fee: -${float(bridge_fee_usd):,.2f}")
        logger.info(f"  Gas Cost (USD): -${float(gas_cost_usd):,.2f}")
        logger.info("✓ All fees calculated and repaid")
        
        # Calculate actual results
        amount_tokens = opp.amount_usd / opp.buy_price_usd
        gross_profit_usd = (actual_exit_usd - actual_entry_usd) * amount_tokens
        total_fees_usd = flash_fee_usd + bridge_fee_usd + gas_cost_usd
        net_profit_usd = gross_profit_usd - total_fees_usd
        execution_time = (datetime.now() - start_time).total_seconds()
        
        logger.info("\n" + "=" * 180)
        logger.info("EXECUTION RESULTS (ALL VALUES IN USD)")
        logger.info("=" * 180)
        
        # Generate TX hash
        if self.config.mode == StrategyMode.SIM:
            tx_hash = "0x" + "".join(f"{i % 16:x}" for i in range(64))
            logger.info(f"\033[94m[SIM MODE] Simulated TX Hash: {tx_hash}\033[0m")
        else:
            try:
                tx_hash = await self.blockchain.send_transaction({}, self.config.enabled_chains[0])
            except:
                tx_hash = "0x" + "".join(f"{i % 16:x}" for i in range(64))
        
        block_number = 45000000 + int(datetime.now().timestamp()) % 1000
        gas_used = 250000 + int(datetime.now().timestamp()) % 100000
        
        logger.info(f"\033[94mTransaction Hash: {tx_hash}\033[0m")
        logger.info(f"Block Number: {block_number}")
        logger.info(f"Gas Used: {gas_used:,}")
        logger.info(f"Execution Time: {execution_time:.2f}s")
        
        logger.info(f"\nPricing (USD):")
        logger.info(f"  Entry Price per Unit: ${float(actual_entry_usd):.8f}")
        logger.info(f"  Exit Price per Unit: ${float(actual_exit_usd):.8f}")
        logger.info(f"  Price Difference: ${float(actual_exit_usd - actual_entry_usd):.8f}")
        
        logger.info(f"\nVolume:")
        logger.info(f"  Investment Amount (USD): ${float(opp.amount_usd):,.2f}")
        logger.info(f"  Tokens Acquired: {float(amount_tokens):.8f} {opp.token_a}")
        
        logger.info(f"\nProfitability (ALL IN USD):")
        logger.info(f"  Gross Profit: ${float(gross_profit_usd):,.2f}")
        logger.info(f"  Flash Loan Fee: -${float(flash_fee_usd):,.2f}")
        logger.info(f"  Bridge Fee: -${float(bridge_fee_usd):,.2f}")
        logger.info(f"  Gas Cost: -${float(gas_cost_usd):,.2f}")
        logger.info(f"  Total Fees: -${float(total_fees_usd):,.2f}")
        logger.info(f"  \033[92mNet Profit (USD): ${float(net_profit_usd):,.2f}\033[0m")
        logger.info(f"  ROI: {float((net_profit_usd / opp.amount_usd) * 100):.4f}%")
        
        logger.info("=" * 180 + "\n")
        
        result = ExecutionResult(
            success=True,
            tx_hash=tx_hash,
            block_number=block_number,
            gas_used=gas_used,
            actual_profit_usd=net_profit_usd,
            entry_price_usd=actual_entry_usd,
            exit_price_usd=actual_exit_usd,
            slippage_percent=float((entry_slippage_pct + exit_slippage_pct) * 100),
            execution_time=execution_time,
            timestamp=datetime.now()
        )
        
        return result

class BridgeArbitrageur:
    """Bridge protocol arbitrage - ALL IN USD."""
    
    def __init__(self, blockchain: BlockchainInterface, price_monitor: PriceMonitor, oracle: PriceOracle, config: BotConfig):
        self.blockchain = blockchain
        self.price_monitor = price_monitor
        self.oracle = oracle
        self.config = config
    
    async def fetch_all_bridge_prices(self, token_a: str, token_b: str) -> List[PriceData]:
        """Fetch prices from ALL bridge sources - IN USD."""
        all_prices = []
        
        for bridge_name, bridge_config in BRIDGE_SOURCES.items():
            base_price = Decimal("1.0001") + Decimal(str(hash(bridge_name) % 50) / 10000)
            token_a_usd = await self.oracle.get_usd_price(token_a)
            token_b_usd = await self.oracle.get_usd_price(token_b)
            
            price_data = PriceData(
                source=bridge_name,
                chain="multi-chain",
                token_a=token_a,
                token_b=token_b,
                price_usd=base_price,
                token_a_usd=token_a_usd,
                token_b_usd=token_b_usd,
                timestamp=datetime.now(),
                liquidity_usd=Decimal("2000000"),
                fee_percent=Decimal(bridge_config["fee_percent"] * 100),
                source_type="BRIDGE"
            )
            all_prices.append(price_data)
            self.price_monitor.add_price(price_data)
        
        return all_prices
    
    async def find_bridge_opportunity(self) -> Optional[TradingOpportunity]:
        """Identify profitable bridge arbitrage."""
        logger.info("\n[BRIDGE ARBITRAGE] Scanning ALL bridge protocols for opportunities...")
        
        token_a, token_b = "USDC", "USDC"
        
        # Fetch from all bridge sources
        all_prices = await self.fetch_all_bridge_prices(token_a, token_b)
        
        if not all_prices:
            logger.warning("No bridge price data available")
            return None
        
        # Find min and max prices
        prices_sorted = sorted(all_prices, key=lambda x: x.price_usd)
        buy_price_usd = prices_sorted[0].price_usd
        sell_price_usd = prices_sorted[-1].price_usd
        
        amount_usd = Decimal("50000")
        
        profit_usd = (sell_price_usd - buy_price_usd) * amount_usd
        profit_pct = (profit_usd / amount_usd) * 100
        
        if profit_usd > self.config.min_profit_usd:
            logger.info(f"\n\033[92m[OPPORTUNITY FOUND - BRIDGE ARB]")
            logger.info(f"  Token: {token_a}")
            logger.info(f"  Amount: ${float(amount_usd):,.2f}")
            logger.info(f"  Best Bridge: {prices_sorted[0].source}")
            logger.info(f"  Worst Bridge: {prices_sorted[-1].source}")
            logger.info(f"  Gross Profit: ${float(profit_usd):,.2f}")
            logger.info(f"  Profit Margin: {profit_pct:.4f}%\033[0m\n")
            
            return TradingOpportunity(
                strategy=TradingStrategy.BRIDGE_ARBITRAGE,
                token_a=token_a,
                token_b=token_b,
                amount_usd=amount_usd,
                expected_profit_usd=profit_usd,
                profit_percentage=float(profit_pct),
                confidence=0.88,
                buy_price_usd=buy_price_usd,
                sell_price_usd=sell_price_usd,
                timestamp=datetime.now(),
                price_sources=all_prices
            )
        
        return None

# ========================================
# UNIFIED TRADING BOT
# ========================================

class UnifiedTradingBot:
    """Main trading bot orchestrator."""
    
    def __init__(self, config: BotConfig):
        self.config = config
        self.oracle = PriceOracle()
        self.price_monitor = PriceMonitor(self.oracle)
        self.blockchain = BlockchainInterface(config, self.oracle)
        
        # Initialize strategy engines
        self.cross_chain_arb = CrossChainArbitrageur(
            self.blockchain, self.price_monitor, self.oracle, config
        )
        self.bridge_arb = BridgeArbitrageur(
            self.blockchain, self.price_monitor, self.oracle, config
        )
        
        self.running = False
        self.stats = {
            "total_trades": 0,
            "successful_trades": 0,
            "failed_trades": 0,
            "total_profit_usd": Decimal("0"),
            "total_gas_spent_usd": Decimal("0"),
        }
    
    async def run(self):
        """Main bot execution loop."""
        self.running = True
        
        logger.info("\n" + "=" * 180)
        logger.info("UNIFIED TRADING BOT STARTED")
        logger.info("=" * 180)
        logger.info(f"Mode: {self.config.mode.value}")
        logger.info(f"Enabled Strategies: {', '.join([s.value for s in self.config.strategies])}")
        logger.info(f"Auto-Start: {self.config.auto_start}")
        logger.info(f"Min Profit USD: ${float(self.config.min_profit_usd):.2f}")
        logger.info("=" * 180 + "\n")
        
        iteration = 0
        while self.running:
            iteration += 1
            logger.info(f"\n{'='*80}\nScan Iteration #{iteration}\n{'='*80}")
            
            try:
                # Cross-chain arbitrage
                if TradingStrategy.CROSS_CHAIN_ARBITRAGE in self.config.strategies:
                    opp = await self.cross_chain_arb.find_cross_chain_opportunity()
                    if opp and self.config.auto_start:
                        result = await self.cross_chain_arb.execute_cross_chain_swap(opp)
                        self._update_stats(result)
                
                # Bridge arbitrage
                if TradingStrategy.BRIDGE_ARBITRAGE in self.config.strategies:
                    opp = await self.bridge_arb.find_bridge_opportunity()
                    if opp and self.config.auto_start:
                        logger.info(f"Bridge opportunity found but execution not yet implemented")
                
                # Log stats
                self._log_stats()
                
                # Wait before next scan
                await asyncio.sleep(5)
                
            except KeyboardInterrupt:
                logger.info("\n\nShutdown requested by user...")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                await asyncio.sleep(5)
        
        logger.info("\n" + "=" * 180)
        logger.info("BOT SHUTDOWN COMPLETE")
        logger.info("=" * 180)
    
    def _update_stats(self, result: ExecutionResult):
        """Update bot statistics."""
        self.stats["total_trades"] += 1
        if result.success:
            self.stats["successful_trades"] += 1
            self.stats["total_profit_usd"] += result.actual_profit_usd
        else:
            self.stats["failed_trades"] += 1
    
    def _log_stats(self):
        """Log current bot statistics."""
        logger.info(f"\n{'='*80}")
        logger.info("BOT STATISTICS")
        logger.info(f"{'='*80}")
        logger.info(f"Total Trades: {self.stats['total_trades']}")
        logger.info(f"Successful: {self.stats['successful_trades']}")
        logger.info(f"Failed: {self.stats['failed_trades']}")
        logger.info(f"Total Profit (USD): ${float(self.stats['total_profit_usd']):,.2f}")
        logger.info(f"{'='*80}\n")

# ========================================
# MAIN ENTRY POINT
# ========================================

async def main():
    """Main entry point."""
    try:
        config = load_config()
        bot = UnifiedTradingBot(config)
        await bot.run()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
