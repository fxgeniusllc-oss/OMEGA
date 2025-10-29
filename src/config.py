"""
Configuration loader with RPC fallback support
"""
import os
from typing import Dict, List, Optional
from dotenv import load_dotenv
from .utils.constants import TradingMode, DEX, Strategy, FlashLoanProvider

# Load environment variables
load_dotenv()

class Config:
    """Main configuration class with environment loading"""
    
    def __init__(self):
        """Initialize configuration from environment variables"""
        
        # Trading Mode
        self.mode = os.getenv('MODE', 'DEV')
        self.auto_start_arbitrage = os.getenv('AUTO_START_ARBITRAGE', 'false').lower() == 'true'
        self.auto_trading_enabled = os.getenv('AUTO_TRADING_ENABLED', 'false').lower() == 'true'
        self.live_execution = os.getenv('LIVE_EXECUTION', 'false').lower() == 'true'
        
        # Addresses
        self.bot_address = os.getenv('BOT_ADDRESS', '')
        self.executor_address = os.getenv('EXECUTOR_ADDRESS', '')
        self.private_key = os.getenv('PRIVATE_KEY', '')
        
        # Chain Configuration
        self.enabled_chains = self._load_enabled_chains()
        
        # RPC URLs with fallback
        self.rpc_urls = self._load_rpc_urls()
        
        # DEX Routers
        self.dex_routers = self._load_dex_routers()
        
        # Active DEXs
        self.active_dexs = self._load_active_dexs()
        
        # Active Strategies
        self.active_strategies = self._load_active_strategies()
        
        # Token Addresses
        self.token_addresses = self._load_token_addresses()
        
        # Flash Loan Configuration
        self.flashloan_provider = os.getenv('FLASHLOAN_PROVIDER', 'BALANCER_VAULT')
        self.max_flashloan_percent = float(os.getenv('MAX_FLASHLOAN_PERCENT_POOL_TVL', '10'))
        
        # Risk Management
        self.min_profit_usd = float(os.getenv('MIN_PROFIT_USD', '15'))
        self.min_liquidity_usd = float(os.getenv('MIN_LIQUIDITY_USD', '50000'))
        self.max_trade_size_usd = float(os.getenv('MAX_TRADE_SIZE_USD', '2000000'))
        self.min_trade_size_usd = float(os.getenv('MIN_TRADE_SIZE_USD', '10000'))
        self.slippage_bps = int(os.getenv('SLIPPAGE_BPS', '50'))
        self.gas_price_multiplier = float(os.getenv('GAS_PRICE_MULTIPLIER', '1.2'))
        
        # Performance
        self.scan_cycle_interval_ms = int(os.getenv('SCAN_CYCLE_INTERVAL_MS', '5000'))
        self.max_concurrent_scans = int(os.getenv('MAX_CONCURRENT_SCANS', '10'))
        self.confidence_threshold = float(os.getenv('CONFIDENCE_THRESHOLD', '0.55'))
        
        # API Keys
        self.polygonscan_api_key = os.getenv('POLYGONSCAN_API_KEY', '')
        self.coingecko_api_key = os.getenv('COINGECKO_API_KEY', '')
        self.telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN', '')
        self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID', '')
        
        # Logging
        self.log_file = os.getenv('LOG_FILE', 'trading_bot.log')
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
    
    def _load_enabled_chains(self) -> List[str]:
        """Load enabled chains from environment"""
        chains = []
        chain_flags = {
            'POLYGON': os.getenv('POLYGON_ENABLED', 'false').lower() == 'true',
            'ETHEREUM': os.getenv('ETHEREUM_ENABLED', 'false').lower() == 'true',
            'ARBITRUM': os.getenv('ARBITRUM_ENABLED', 'false').lower() == 'true',
            'OPTIMISM': os.getenv('OPTIMISM_ENABLED', 'false').lower() == 'true',
            'BASE': os.getenv('BASE_ENABLED', 'false').lower() == 'true',
            'BSC': os.getenv('BSC_ENABLED', 'false').lower() == 'true',
            'SOLANA': os.getenv('SOLANA_ENABLED', 'false').lower() == 'true',
        }
        
        for chain, enabled in chain_flags.items():
            if enabled:
                chains.append(chain)
        
        return chains if chains else ['POLYGON']  # Default to POLYGON if none enabled
    
    def _load_rpc_urls(self) -> Dict[str, List[str]]:
        """Load RPC URLs with automatic fallback support"""
        rpc_urls = {}
        
        # POLYGON - Multiple fallbacks
        polygon_rpcs = []
        if os.getenv('INFURA_POLYGON_RPC'):
            polygon_rpcs.append(os.getenv('INFURA_POLYGON_RPC'))
        if os.getenv('QUICKNODE_RPC_URL'):
            polygon_rpcs.append(os.getenv('QUICKNODE_RPC_URL'))
        if os.getenv('ALCHEMY_RPC_URL'):
            polygon_rpcs.append(os.getenv('ALCHEMY_RPC_URL'))
        if polygon_rpcs:
            rpc_urls['POLYGON'] = polygon_rpcs
        
        # ETHEREUM
        eth_rpcs = []
        if os.getenv('ETHEREUM_RPC_URL'):
            eth_rpcs.append(os.getenv('ETHEREUM_RPC_URL'))
        if os.getenv('INFURA_ETHEREUM_RPC'):
            eth_rpcs.append(os.getenv('INFURA_ETHEREUM_RPC'))
        if eth_rpcs:
            rpc_urls['ETHEREUM'] = eth_rpcs
        
        # ARBITRUM
        arb_rpcs = []
        if os.getenv('ARBITRUM_RPC_URL'):
            arb_rpcs.append(os.getenv('ARBITRUM_RPC_URL'))
        if os.getenv('INFURA_ARBITRUM_RPC'):
            arb_rpcs.append(os.getenv('INFURA_ARBITRUM_RPC'))
        if arb_rpcs:
            rpc_urls['ARBITRUM'] = arb_rpcs
        
        # OPTIMISM
        opt_rpcs = []
        if os.getenv('OPTIMISM_RPC_URL'):
            opt_rpcs.append(os.getenv('OPTIMISM_RPC_URL'))
        if os.getenv('INFURA_OPTIMISM_RPC'):
            opt_rpcs.append(os.getenv('INFURA_OPTIMISM_RPC'))
        if opt_rpcs:
            rpc_urls['OPTIMISM'] = opt_rpcs
        
        # BASE
        base_rpcs = []
        if os.getenv('BASE_RPC_URL'):
            base_rpcs.append(os.getenv('BASE_RPC_URL'))
        if os.getenv('INFURA_BASE_RPC'):
            base_rpcs.append(os.getenv('INFURA_BASE_RPC'))
        if base_rpcs:
            rpc_urls['BASE'] = base_rpcs
        
        # BSC
        bsc_rpcs = []
        if os.getenv('BSC_RPC_URL'):
            bsc_rpcs.append(os.getenv('BSC_RPC_URL'))
        if os.getenv('INFURA_BSC_RPC'):
            bsc_rpcs.append(os.getenv('INFURA_BSC_RPC'))
        if bsc_rpcs:
            rpc_urls['BSC'] = bsc_rpcs
        
        # SOLANA
        solana_rpcs = []
        if os.getenv('SOLANA_ALCHEMY_RPC'):
            solana_rpcs.append(os.getenv('SOLANA_ALCHEMY_RPC'))
        if os.getenv('SOLANA_QUICKNODE_RPC'):
            solana_rpcs.append(os.getenv('SOLANA_QUICKNODE_RPC'))
        if solana_rpcs:
            rpc_urls['SOLANA'] = solana_rpcs
        
        return rpc_urls
    
    def _load_dex_routers(self) -> Dict[str, str]:
        """Load DEX router addresses from environment"""
        return {
            'QUICKSWAP': os.getenv('QUICKSWAP_ROUTER', ''),
            'SUSHISWAP': os.getenv('SUSHISWAP_ROUTER', ''),
            'UNISWAP_V3': os.getenv('UNISWAP_V3_ROUTER', ''),
            'PARASWAP': os.getenv('PARASWAP_ROUTER', ''),
            'ONEINCH': os.getenv('ONEINCH_ROUTER', ''),
            'BALANCER_V2': os.getenv('BALANCER_V2_VAULT', ''),
            'CURVE': os.getenv('CURVE_ROUTER', ''),
            'DODO': os.getenv('DODO_ROUTER', ''),
            'KYBER': os.getenv('KYBER_ROUTER', ''),
        }
    
    def _load_active_dexs(self) -> List[str]:
        """Load active DEXs from environment"""
        dexs_str = os.getenv('ACTIVE_DEXS', 'quickswap,uniswap_v3,sushiswap')
        return [dex.strip().upper() for dex in dexs_str.split(',') if dex.strip()]
    
    def _load_active_strategies(self) -> List[str]:
        """Load active strategies from environment"""
        strategies_str = os.getenv('ACTIVE_STRATEGIES', 'CROSS_CHAIN_ARBITRAGE')
        return [s.strip() for s in strategies_str.split(',') if s.strip()]
    
    def _load_token_addresses(self) -> Dict[str, str]:
        """Load token addresses from environment"""
        return {
            'WMATIC': os.getenv('WMATIC', ''),
            'USDC': os.getenv('USDC', ''),
            'USDT': os.getenv('USDT', ''),
            'DAI': os.getenv('DAI', ''),
            'WETH': os.getenv('WETH', ''),
            'WBTC': os.getenv('WBTC', ''),
            'LINK': os.getenv('LINK', ''),
            'AAVE': os.getenv('AAVE', ''),
            'UNI': os.getenv('UNI', ''),
        }
    
    def get_rpc_url(self, chain: str, index: int = 0) -> Optional[str]:
        """Get RPC URL for a chain with fallback support"""
        if chain in self.rpc_urls and len(self.rpc_urls[chain]) > index:
            return self.rpc_urls[chain][index]
        return None
    
    def get_all_rpc_urls(self, chain: str) -> List[str]:
        """Get all RPC URLs for a chain"""
        return self.rpc_urls.get(chain, [])
    
    def validate(self) -> bool:
        """Validate configuration"""
        errors = []
        
        if not self.bot_address:
            errors.append("BOT_ADDRESS not set")
        
        if not self.executor_address:
            errors.append("EXECUTOR_ADDRESS not set")
        
        if self.live_execution and not self.private_key:
            errors.append("PRIVATE_KEY required for live execution")
        
        if not self.enabled_chains:
            errors.append("No chains enabled")
        
        for chain in self.enabled_chains:
            if chain not in self.rpc_urls or not self.rpc_urls[chain]:
                errors.append(f"No RPC URL configured for {chain}")
        
        if errors:
            print("❌ Configuration Errors:")
            for error in errors:
                print(f"  - {error}")
            return False
        
        return True

# Global config instance
config = Config()
