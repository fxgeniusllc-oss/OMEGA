"""Configuration loader for the DeFi Trading Bot."""

import os
from decimal import Decimal
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for loading environment variables."""
    
    # Trading Mode
    MODE = os.getenv("MODE", "DEV")
    AUTO_START_ARBITRAGE = os.getenv("AUTO_START_ARBITRAGE", "false").lower() == "true"
    AUTO_TRADING_ENABLED = os.getenv("AUTO_TRADING_ENABLED", "false").lower() == "true"
    LIVE_EXECUTION = os.getenv("LIVE_EXECUTION", "false").lower() == "true"
    
    # Addresses
    BOT_ADDRESS = os.getenv("BOT_ADDRESS", "")
    EXECUTOR_ADDRESS = os.getenv("EXECUTOR_ADDRESS", "")
    PRIVATE_KEY = os.getenv("PRIVATE_KEY", "")
    
    # RPC URLs
    POLYGON_RPC = os.getenv("INFURA_POLYGON_RPC", "")
    POLYGON_RPC_WS = os.getenv("INFURA_POLYGON_RPC_WS", "")
    ETHEREUM_RPC = os.getenv("ETHEREUM_RPC_URL", "")
    ARBITRUM_RPC = os.getenv("ARBITRUM_RPC_URL", "")
    OPTIMISM_RPC = os.getenv("OPTIMISM_RPC_URL", "")
    BASE_RPC = os.getenv("BASE_RPC_URL", "")
    
    # Chain Configuration
    POLYGON_ENABLED = os.getenv("POLYGON_ENABLED", "true").lower() == "true"
    ETHEREUM_ENABLED = os.getenv("ETHEREUM_ENABLED", "false").lower() == "true"
    ARBITRUM_ENABLED = os.getenv("ARBITRUM_ENABLED", "false").lower() == "true"
    OPTIMISM_ENABLED = os.getenv("OPTIMISM_ENABLED", "false").lower() == "true"
    
    # Risk Management
    MIN_PROFIT_USD = Decimal(os.getenv("MIN_PROFIT_USD", "15"))
    MIN_LIQUIDITY_USD = Decimal(os.getenv("MIN_LIQUIDITY_USD", "50000"))
    MAX_TRADE_SIZE_USD = Decimal(os.getenv("MAX_TRADE_SIZE_USD", "2000000"))
    MIN_TRADE_SIZE_USD = Decimal(os.getenv("MIN_TRADE_SIZE_USD", "10000"))
    SLIPPAGE_BPS = int(os.getenv("SLIPPAGE_BPS", "50"))
    GAS_PRICE_MULTIPLIER = Decimal(os.getenv("GAS_PRICE_MULTIPLIER", "1.2"))
    
    # Performance
    SCAN_CYCLE_INTERVAL_MS = int(os.getenv("SCAN_CYCLE_INTERVAL_MS", "5000"))
    MAX_CONCURRENT_SCANS = int(os.getenv("MAX_CONCURRENT_SCANS", "10"))
    CONFIDENCE_THRESHOLD = Decimal(os.getenv("CONFIDENCE_THRESHOLD", "0.55"))
    
    # API Keys
    POLYGONSCAN_API_KEY = os.getenv("POLYGONSCAN_API_KEY", "")
    COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY", "")
    
    # Logging
    LOG_FILE = os.getenv("LOG_FILE", "trading_bot.log")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def get_enabled_chains(cls) -> list:
        """Get list of enabled chains."""
        chains = []
        if cls.POLYGON_ENABLED:
            chains.append("polygon")
        if cls.ETHEREUM_ENABLED:
            chains.append("ethereum")
        if cls.ARBITRUM_ENABLED:
            chains.append("arbitrum")
        if cls.OPTIMISM_ENABLED:
            chains.append("optimism")
        return chains
    
    @classmethod
    def get_rpc_url(cls, chain: str) -> Optional[str]:
        """Get RPC URL for a chain."""
        rpc_map = {
            "polygon": cls.POLYGON_RPC,
            "ethereum": cls.ETHEREUM_RPC,
            "arbitrum": cls.ARBITRUM_RPC,
            "optimism": cls.OPTIMISM_RPC,
        }
        return rpc_map.get(chain)
