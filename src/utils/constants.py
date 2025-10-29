"""Constants and enums for the trading bot."""
from enum import Enum


class TradingMode(Enum):
    """Trading mode enumeration."""
    LIVE = "LIVE"
    DEV = "DEV"
    SIM = "SIM"


class StrategyType(Enum):
    """Strategy type enumeration."""
    MEMPOOL_WATCHING = "MEMPOOL_WATCHING"
    CROSS_CHAIN_ARBITRAGE = "CROSS_CHAIN_ARBITRAGE"
    PUMP_PREDICTION = "PUMP_PREDICTION"
    MARKET_MAKING = "MARKET_MAKING"
    STATISTICAL_ARBITRAGE = "STATISTICAL_ARBITRAGE"
    GAMMA_SCALPING = "GAMMA_SCALPING"
    FUNDING_RATE = "FUNDING_RATE"
    VOLATILITY_ARBITRAGE = "VOLATILITY_ARBITRAGE"
    BRIDGE_ARBITRAGE = "BRIDGE_ARBITRAGE"


class FlashLoanProvider(Enum):
    """Flash loan provider enumeration."""
    BALANCER = "BALANCER"
    AAVE = "AAVE"


# Chain IDs
CHAIN_IDS = {
    "POLYGON": 137,
    "ETHEREUM": 1,
    "ARBITRUM": 42161,
    "OPTIMISM": 10,
}

# Fee constants
BALANCER_FLASH_LOAN_FEE = 0.0001  # 0.01%
AAVE_FLASH_LOAN_FEE = 0.0009  # 0.09%

# Trading constants
MIN_PROFIT_THRESHOLD = 10  # Minimum profit in USD
MAX_SLIPPAGE = 0.01  # 1%
DEFAULT_GAS_LIMIT = 500000

# Risk management
KELLY_FRACTION = 0.25  # Conservative Kelly fraction
MAX_PORTFOLIO_RISK = 0.20  # 20% max portfolio risk
