"""
Constants and enums for the trading bot
"""
from enum import Enum

# Chain IDs
CHAIN_IDS = {
    'POLYGON': 137,
    'ETHEREUM': 1,
    'ARBITRUM': 42161,
    'OPTIMISM': 10,
    'BASE': 8453,
    'BSC': 56,
}

# DEX Names
class DEX(Enum):
    QUICKSWAP = "quickswap"
    UNISWAP_V3 = "uniswap_v3"
    SUSHISWAP = "sushiswap"
    BALANCER = "balancer"
    CURVE = "curve"
    PARASWAP = "paraswap"
    ONEINCH = "oneinch"
    DODO = "dodo"
    KYBER = "kyber"

# Strategy Types
class Strategy(Enum):
    CROSS_CHAIN_ARBITRAGE = "CROSS_CHAIN_ARBITRAGE"
    BRIDGE_ARBITRAGE = "BRIDGE_ARBITRAGE"
    MEMPOOL_WATCHING = "MEMPOOL_WATCHING"

# Flash Loan Providers
class FlashLoanProvider(Enum):
    BALANCER_VAULT = "BALANCER_VAULT"
    AAVE = "AAVE"
    DYDX = "DYDX"

# Trading Modes
class TradingMode(Enum):
    LIVE = "LIVE"
    DEV = "DEV"
    SIM = "SIM"

# Chain Explorer URLs
EXPLORER_URLS = {
    'POLYGON': 'https://polygonscan.com',
    'ETHEREUM': 'https://etherscan.io',
    'ARBITRUM': 'https://arbiscan.io',
    'OPTIMISM': 'https://optimistic.etherscan.io',
    'BASE': 'https://basescan.org',
    'BSC': 'https://bscscan.com',
}

# Standard token decimals
TOKEN_DECIMALS = {
    'WMATIC': 18,
    'USDC': 6,
    'USDT': 6,
    'DAI': 18,
    'WETH': 18,
    'WBTC': 8,
    'LINK': 18,
    'AAVE': 18,
    'UNI': 18,
}

# Gas limits
GAS_LIMITS = {
    'SWAP': 200000,
    'FLASHLOAN': 500000,
    'ARBITRAGE': 800000,
}
