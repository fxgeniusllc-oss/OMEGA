"""
Configuration loader for the trading bot.
Loads settings from environment variables.
"""
import os
from dotenv import load_dotenv
from typing import List

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for trading bot settings"""
    
    # Trading Mode
    MODE = os.getenv('MODE', 'DEV')
    AUTO_START_ARBITRAGE = os.getenv('AUTO_START_ARBITRAGE', 'false').lower() == 'true'
    AUTO_TRADING_ENABLED = os.getenv('AUTO_TRADING_ENABLED', 'false').lower() == 'true'
    LIVE_EXECUTION = os.getenv('LIVE_EXECUTION', 'false').lower() == 'true'
    
    # Addresses
    BOT_ADDRESS = os.getenv('BOT_ADDRESS', '')
    EXECUTOR_ADDRESS = os.getenv('EXECUTOR_ADDRESS', '')
    PRIVATE_KEY = os.getenv('PRIVATE_KEY', '')
    
    # RPC URLs
    INFURA_POLYGON_RPC = os.getenv('INFURA_POLYGON_RPC', '')
    ETHEREUM_RPC_URL = os.getenv('ETHEREUM_RPC_URL', '')
    ARBITRUM_RPC_URL = os.getenv('ARBITRUM_RPC_URL', '')
    OPTIMISM_RPC_URL = os.getenv('OPTIMISM_RPC_URL', '')
    BASE_RPC_URL = os.getenv('BASE_RPC_URL', '')
    
    # Chain Configuration
    POLYGON_ENABLED = os.getenv('POLYGON_ENABLED', 'true').lower() == 'true'
    ETHEREUM_ENABLED = os.getenv('ETHEREUM_ENABLED', 'false').lower() == 'true'
    ARBITRUM_ENABLED = os.getenv('ARBITRUM_ENABLED', 'false').lower() == 'true'
    OPTIMISM_ENABLED = os.getenv('OPTIMISM_ENABLED', 'false').lower() == 'true'
    BASE_ENABLED = os.getenv('BASE_ENABLED', 'false').lower() == 'true'
    
    # DEX Configuration
    ACTIVE_DEXS = os.getenv('ACTIVE_DEXS', 'quickswap,uniswap_v3').split(',')
    ACTIVE_STRATEGIES = os.getenv('ACTIVE_STRATEGIES', 'CROSS_CHAIN_ARBITRAGE').split(',')
    
    # Risk Management
    MIN_PROFIT_USD = float(os.getenv('MIN_PROFIT_USD', '15'))
    MIN_LIQUIDITY_USD = float(os.getenv('MIN_LIQUIDITY_USD', '50000'))
    MAX_TRADE_SIZE_USD = float(os.getenv('MAX_TRADE_SIZE_USD', '2000000'))
    MIN_TRADE_SIZE_USD = float(os.getenv('MIN_TRADE_SIZE_USD', '10000'))
    SLIPPAGE_BPS = int(os.getenv('SLIPPAGE_BPS', '50'))
    GAS_PRICE_MULTIPLIER = float(os.getenv('GAS_PRICE_MULTIPLIER', '1.2'))
    
    # Performance
    SCAN_CYCLE_INTERVAL_MS = int(os.getenv('SCAN_CYCLE_INTERVAL_MS', '5000'))
    MAX_CONCURRENT_SCANS = int(os.getenv('MAX_CONCURRENT_SCANS', '10'))
    CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', '0.55'))
    
    # Logging
    LOG_FILE = os.getenv('LOG_FILE', 'trading_bot.log')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def get_active_strategies(cls) -> List[str]:
        """Get list of active strategies"""
        return [s.strip() for s in cls.ACTIVE_STRATEGIES if s.strip()]
    
    @classmethod
    def get_active_dexs(cls) -> List[str]:
        """Get list of active DEXs"""
        return [d.strip() for d in cls.ACTIVE_DEXS if d.strip()]
    
    @classmethod
    def is_simulation_mode(cls) -> bool:
        """Check if running in simulation mode"""
        return not cls.LIVE_EXECUTION
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        errors = []
        
        if cls.LIVE_EXECUTION:
            if not cls.BOT_ADDRESS:
                errors.append("BOT_ADDRESS is required for live execution")
            if not cls.PRIVATE_KEY:
                errors.append("PRIVATE_KEY is required for live execution")
        
        if not cls.INFURA_POLYGON_RPC and cls.POLYGON_ENABLED:
            errors.append("INFURA_POLYGON_RPC is required when POLYGON is enabled")
        
        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")
        
        return True
