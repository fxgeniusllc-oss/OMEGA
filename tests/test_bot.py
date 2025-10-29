"""Tests for the main trading bot."""

import pytest
from decimal import Decimal
from src.bot import UnifiedTradingBot
from src.utils.constants import DEX_SOURCES, BRIDGE_SOURCES, CEX_SOURCES


@pytest.mark.asyncio
async def test_bot_initialization():
    """Test bot initialization."""
    bot = UnifiedTradingBot()
    
    # Bot should be initialized
    assert bot is not None
    assert bot.oracle is not None
    assert bot.logger is not None


@pytest.mark.asyncio
async def test_initialize_sources():
    """Test source initialization."""
    bot = UnifiedTradingBot()
    
    # Should not raise any errors
    await bot._initialize_sources()


@pytest.mark.asyncio
async def test_find_best_opportunity():
    """Test finding best arbitrage opportunity."""
    bot = UnifiedTradingBot()
    
    # Create mock comparisons
    comparisons = [
        {
            "source": "DEX1",
            "price_usd": Decimal("2347.50"),
            "fee_pct": Decimal("0.0001")
        },
        {
            "source": "DEX2",
            "price_usd": Decimal("2349.00"),
            "fee_pct": Decimal("0.0001")
        }
    ]
    
    opportunity = bot._find_best_opportunity(comparisons)
    
    # Should find an opportunity
    assert opportunity is not None
    assert "buy_source" in opportunity
    assert "sell_source" in opportunity
    assert "price_diff_pct" in opportunity
    assert "net_profit_pct" in opportunity


@pytest.mark.asyncio
async def test_find_best_opportunity_unprofitable():
    """Test finding opportunity with no profit."""
    bot = UnifiedTradingBot()
    
    # Create mock comparisons with minimal difference
    comparisons = [
        {
            "source": "DEX1",
            "price_usd": Decimal("2347.50"),
            "fee_pct": Decimal("0.001")
        },
        {
            "source": "DEX2",
            "price_usd": Decimal("2347.51"),
            "fee_pct": Decimal("0.001")
        }
    ]
    
    opportunity = bot._find_best_opportunity(comparisons)
    
    # Should not find profitable opportunity
    assert opportunity is None


@pytest.mark.asyncio
async def test_estimate_gas_cost_usd():
    """Test gas cost estimation."""
    bot = UnifiedTradingBot()
    
    # Test different chains
    gas_polygon = await bot._estimate_gas_cost_usd("polygon")
    assert gas_polygon > Decimal("0")
    assert gas_polygon < Decimal("5")
    
    gas_ethereum = await bot._estimate_gas_cost_usd("ethereum")
    assert gas_ethereum > Decimal("5")
    
    gas_unknown = await bot._estimate_gas_cost_usd("unknown")
    assert gas_unknown > Decimal("0")


@pytest.mark.asyncio
async def test_find_best_bridge():
    """Test finding best bridge between chains."""
    bot = UnifiedTradingBot()
    
    # Test finding bridge
    bridge = bot._find_best_bridge("ethereum", "polygon")
    
    # Should find a bridge
    assert bridge is not None
    assert "name" in bridge
    assert "fee" in bridge
    
    # Bridge name should be in BRIDGE_SOURCES
    assert bridge["name"] in BRIDGE_SOURCES


@pytest.mark.asyncio
async def test_find_best_bridge_no_route():
    """Test finding bridge with no route available."""
    bot = UnifiedTradingBot()
    
    # Test with invalid chains
    bridge = bot._find_best_bridge("invalid1", "invalid2")
    
    # Should not find a bridge
    assert bridge is None


def test_dex_sources_structure():
    """Test DEX sources configuration structure."""
    # Should have multiple chains
    assert len(DEX_SOURCES) >= 4
    
    # Should have polygon
    assert "polygon" in DEX_SOURCES
    
    # Each DEX should have required fields
    for chain, dexs in DEX_SOURCES.items():
        for dex_name, dex_config in dexs.items():
            assert "rpc_method" in dex_config
            assert "fee_tier" in dex_config
            assert "liquidity_mult" in dex_config


def test_bridge_sources_structure():
    """Test bridge sources configuration structure."""
    # Should have 5 bridges
    assert len(BRIDGE_SOURCES) == 5
    
    # Each bridge should have required fields
    for bridge_name, bridge_config in BRIDGE_SOURCES.items():
        assert "fee" in bridge_config
        assert "router" in bridge_config
        assert "chains" in bridge_config
        assert isinstance(bridge_config["chains"], list)


def test_cex_sources_structure():
    """Test CEX sources configuration structure."""
    # Should have 3 CEXs
    assert len(CEX_SOURCES) == 3
    
    # Should have Binance, Coinbase, Kraken
    assert "Binance" in CEX_SOURCES
    assert "Coinbase" in CEX_SOURCES
    assert "Kraken" in CEX_SOURCES
    
    # Each CEX should have required fields
    for cex_name, cex_config in CEX_SOURCES.items():
        assert "api_url" in cex_config
        assert "fee" in cex_config
        assert "pairs" in cex_config


def test_total_source_count():
    """Test total number of sources matches specification."""
    # Count DEX sources
    total_dex = sum(len(sources) for sources in DEX_SOURCES.values())
    
    # Count bridge sources
    total_bridge = len(BRIDGE_SOURCES)
    
    # Count CEX sources
    total_cex = len(CEX_SOURCES)
    
    # Should have approximately 24 DEX, 5 Bridge, 3 CEX
    assert total_dex >= 20  # At least 20 DEX sources
    assert total_bridge == 5
    assert total_cex == 3
    
    # Total should be 28+
    total = total_dex + total_bridge + total_cex
    assert total >= 28
