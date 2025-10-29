"""Configuration loader for the trading bot."""
import os
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration management for the trading bot."""
    
    # Trading Mode
    MODE: str = os.getenv("MODE", "DEV")  # LIVE, DEV, or SIM
    AUTO_START_ARBITRAGE: bool = os.getenv("AUTO_START_ARBITRAGE", "true").lower() == "true"
    LIVE_EXECUTION: bool = os.getenv("LIVE_EXECUTION", "false").lower() == "true"
    
    # Addresses
    BOT_ADDRESS: str = os.getenv("BOT_ADDRESS", "")
    PRIVATE_KEY: str = os.getenv("PRIVATE_KEY", "")
    
    # RPC Endpoints
    INFURA_POLYGON_RPC: str = os.getenv("INFURA_POLYGON_RPC", "")
    INFURA_ETHEREUM_RPC: str = os.getenv("INFURA_ETHEREUM_RPC", "")
    INFURA_ARBITRUM_RPC: str = os.getenv("INFURA_ARBITRUM_RPC", "")
    INFURA_OPTIMISM_RPC: str = os.getenv("INFURA_OPTIMISM_RPC", "")
    
    # Active Strategies
    ACTIVE_STRATEGIES: List[str] = os.getenv(
        "ACTIVE_STRATEGIES",
        "MEMPOOL_WATCHING,CROSS_CHAIN_ARBITRAGE,PUMP_PREDICTION,MARKET_MAKING,STATISTICAL_ARBITRAGE,GAMMA_SCALPING,FUNDING_RATE,VOLATILITY_ARBITRAGE,BRIDGE_ARBITRAGE"
    ).split(",")
    
    # Flash Loan Configuration
    FLASH_LOAN_PROVIDER: str = os.getenv("FLASH_LOAN_PROVIDER", "BALANCER")
    
    # Risk Management
    SLIPPAGE_TOLERANCE: float = float(os.getenv("SLIPPAGE_TOLERANCE", "0.005"))
    GAS_PRICE_MULTIPLIER: float = float(os.getenv("GAS_PRICE_MULTIPLIER", "1.1"))
    MAX_POSITION_SIZE: float = float(os.getenv("MAX_POSITION_SIZE", "10000"))
    RISK_PER_TRADE: float = float(os.getenv("RISK_PER_TRADE", "0.02"))
    
    # Logging
    LOG_FILE: str = os.getenv("LOG_FILE", "trading_bot.log")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # DEX Configuration
    QUICKSWAP_ROUTER: str = os.getenv("QUICKSWAP_ROUTER", "0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff")
    SUSHISWAP_ROUTER: str = os.getenv("SUSHISWAP_ROUTER", "0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506")
    UNISWAP_V3_ROUTER: str = os.getenv("UNISWAP_V3_ROUTER", "0xE592427A0AEce92De3Edee1F18E0157C05861564")
    BALANCER_V2_VAULT: str = os.getenv("BALANCER_V2_VAULT", "0xBA12222222228d8Ba445958a75a0704d566BF2C8")
    
    # Token Addresses (Polygon)
    WMATIC: str = os.getenv("WMATIC", "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270")
    USDC: str = os.getenv("USDC", "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174")
    USDT: str = os.getenv("USDT", "0xc2132D05D31c914a87C6611C10748AEb04B58e8F")
    DAI: str = os.getenv("DAI", "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063")
    WETH: str = os.getenv("WETH", "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619")
    WBTC: str = os.getenv("WBTC", "0x1BFD67037B42Cf73acF2047067bd4F2C47D9BfD6")
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration."""
        if cls.MODE not in ["LIVE", "DEV", "SIM"]:
            raise ValueError(f"Invalid MODE: {cls.MODE}. Must be LIVE, DEV, or SIM")
        
        if cls.MODE == "LIVE" and not cls.PRIVATE_KEY:
            raise ValueError("PRIVATE_KEY is required for LIVE mode")
        
        if not cls.BOT_ADDRESS:
            raise ValueError("BOT_ADDRESS is required")
        
        return True


# Validate on import
Config.validate()
