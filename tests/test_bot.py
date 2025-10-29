"""Tests for the trading bot."""
import pytest
from decimal import Decimal
from src.bot import (
    PriceOracle,
    StrategyMode,
    TradingStrategy,
    load_config,
    BotConfig,
)


def test_price_oracle():
    """Test PriceOracle initialization."""
    oracle = PriceOracle()
    assert oracle.exchange_rates["USDC"] == Decimal("1.0000")
    assert oracle.exchange_rates["WETH"] == Decimal("2347.50")


@pytest.mark.asyncio
async def test_get_usd_price():
    """Test getting USD price for a token."""
    oracle = PriceOracle()
    price = await oracle.get_usd_price("USDC")
    assert price == Decimal("1.0000")


@pytest.mark.asyncio
async def test_convert_to_usd():
    """Test converting token amount to USD."""
    oracle = PriceOracle()
    amount = Decimal("10")
    usd_value = await oracle.convert_to_usd(amount, "USDC")
    assert usd_value == Decimal("10.0000")


@pytest.mark.asyncio
async def test_convert_from_usd():
    """Test converting USD to token amount."""
    oracle = PriceOracle()
    usd_amount = Decimal("100")
    token_amount = await oracle.convert_from_usd(usd_amount, "USDC")
    assert token_amount == Decimal("100.0000")


def test_strategy_mode_enum():
    """Test StrategyMode enum."""
    assert StrategyMode.LIVE.value == "LIVE"
    assert StrategyMode.DEV.value == "DEV"
    assert StrategyMode.SIM.value == "SIM"


def test_trading_strategy_enum():
    """Test TradingStrategy enum."""
    assert TradingStrategy.CROSS_CHAIN_ARBITRAGE.value == "cross_chain_arbitrage"
    assert TradingStrategy.BRIDGE_ARBITRAGE.value == "bridge_arbitrage"


def test_load_config():
    """Test loading configuration from environment."""
    config = load_config()
    assert isinstance(config, BotConfig)
    assert config.mode in [StrategyMode.LIVE, StrategyMode.DEV, StrategyMode.SIM]
    assert isinstance(config.strategies, list)
    assert config.min_profit_usd > 0
