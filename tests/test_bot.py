"""Basic tests for the trading bot."""
import pytest
import asyncio
from src.bot import UnifiedTradingBot
from src.config import Config
from src.utils.helpers import calculate_kelly_fraction, calculate_position_size


def test_config_loads():
    """Test that configuration loads properly."""
    assert Config.MODE in ["LIVE", "DEV", "SIM"]
    assert Config.BOT_ADDRESS is not None


def test_kelly_fraction():
    """Test Kelly fraction calculation."""
    # Test case: 60% win rate, 2:1 win/loss ratio
    kelly_frac = calculate_kelly_fraction(0.6, 2.0)
    assert 0 < kelly_frac <= 0.25  # Should be capped at 0.25
    
    # Test case: 50% win rate, 1:1 ratio (no edge)
    kelly_frac = calculate_kelly_fraction(0.5, 1.0)
    assert kelly_frac == 0.0


def test_position_size_calculation():
    """Test position size calculation."""
    capital = 10000
    win_prob = 0.7
    expected_profit = 100
    expected_loss = 50
    max_position = 5000
    
    position_size = calculate_position_size(
        capital, win_prob, expected_profit, expected_loss, max_position
    )
    
    assert 0 < position_size <= max_position


@pytest.mark.asyncio
async def test_bot_initialization():
    """Test bot initialization."""
    bot = UnifiedTradingBot()
    
    assert bot.config is not None
    assert bot.blockchain is not None
    assert bot.oracle is not None
    assert bot.position_manager is not None
    assert bot.flash_loan_manager is not None
    assert len(bot.strategies) > 0


@pytest.mark.asyncio
async def test_strategies_enabled():
    """Test that strategies are enabled based on config."""
    bot = UnifiedTradingBot()
    
    # Check that active strategies are enabled
    for strategy_name in Config.ACTIVE_STRATEGIES:
        strategy_name = strategy_name.strip()
        if strategy_name in bot.strategies:
            strategy = bot.strategies[strategy_name]
            assert strategy.enabled is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
