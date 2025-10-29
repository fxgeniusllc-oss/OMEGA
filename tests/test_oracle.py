"""Tests for the PriceOracle class."""

import pytest
from decimal import Decimal
from src.oracle import PriceOracle


@pytest.mark.asyncio
async def test_get_usd_price_stablecoin():
    """Test that stablecoins always return $1."""
    oracle = PriceOracle()
    
    # Test various stablecoins
    usdc_price = await oracle.get_usd_price("USDC")
    assert usdc_price == Decimal("1.0")
    
    usdt_price = await oracle.get_usd_price("USDT")
    assert usdt_price == Decimal("1.0")
    
    dai_price = await oracle.get_usd_price("DAI")
    assert dai_price == Decimal("1.0")


@pytest.mark.asyncio
async def test_get_usd_price_weth():
    """Test getting USD price for WETH."""
    oracle = PriceOracle()
    
    weth_price = await oracle.get_usd_price("WETH")
    
    # WETH should have a price > 0
    assert weth_price > Decimal("0")
    # Should be in reasonable range for ETH
    assert weth_price > Decimal("1000")
    assert weth_price < Decimal("10000")


@pytest.mark.asyncio
async def test_convert_to_usd():
    """Test converting token amount to USD."""
    oracle = PriceOracle()
    
    # Test with stablecoin (should be 1:1)
    usdc_amount = Decimal("100")
    usd_value = await oracle.convert_to_usd(usdc_amount, "USDC")
    assert usd_value == Decimal("100")
    
    # Test with WETH
    weth_amount = Decimal("1")
    usd_value = await oracle.convert_to_usd(weth_amount, "WETH")
    assert usd_value > Decimal("1000")


@pytest.mark.asyncio
async def test_convert_from_usd():
    """Test converting USD to token amount."""
    oracle = PriceOracle()
    
    # Test with stablecoin
    usd_amount = Decimal("100")
    usdc_amount = await oracle.convert_from_usd(usd_amount, "USDC")
    assert usdc_amount == Decimal("100")
    
    # Test with WETH
    usd_amount = Decimal("2347.50")
    weth_amount = await oracle.convert_from_usd(usd_amount, "WETH")
    # Should get approximately 1 WETH
    assert weth_amount > Decimal("0.9")
    assert weth_amount < Decimal("1.1")


@pytest.mark.asyncio
async def test_get_price_comparison():
    """Test getting price comparison from multiple sources."""
    oracle = PriceOracle()
    
    comparisons = await oracle.get_price_comparison("WETH", "USDC", "polygon")
    
    # Should have multiple comparisons
    assert len(comparisons) > 0
    
    # Each comparison should have required fields
    for comp in comparisons:
        assert "source" in comp
        assert "type" in comp
        assert "price_usd" in comp
        assert "token_a_usd" in comp
        assert "token_b_usd" in comp
        assert "liquidity_usd" in comp
        assert "fee_pct" in comp
        
        # Values should be positive
        assert comp["price_usd"] > Decimal("0")
        assert comp["liquidity_usd"] > Decimal("0")


@pytest.mark.asyncio
async def test_price_cache():
    """Test that price caching works."""
    oracle = PriceOracle()
    
    # Get price first time
    price1 = await oracle.get_usd_price("WETH")
    
    # Get price second time (should use cache)
    price2 = await oracle.get_usd_price("WETH")
    
    # Prices should be identical (from cache)
    assert price1 == price2
    
    # Cache key should exist
    cache_key = "polygon_WETH"
    assert cache_key in oracle.price_cache


@pytest.mark.asyncio
async def test_median_calculation():
    """Test median price calculation."""
    oracle = PriceOracle()
    
    # Test odd number of prices
    prices_odd = [Decimal("100"), Decimal("110"), Decimal("105")]
    median_odd = oracle._calculate_median(prices_odd)
    assert median_odd == Decimal("105")
    
    # Test even number of prices
    prices_even = [Decimal("100"), Decimal("110"), Decimal("105"), Decimal("115")]
    median_even = oracle._calculate_median(prices_even)
    assert median_even == Decimal("107.5")
    
    # Test empty list
    median_empty = oracle._calculate_median([])
    assert median_empty == Decimal("0")


@pytest.mark.asyncio
async def test_fallback_price():
    """Test fallback price mechanism."""
    oracle = PriceOracle()
    
    # Test known token
    weth_fallback = await oracle._get_fallback_price("WETH")
    assert weth_fallback > Decimal("0")
    
    # Test unknown token
    unknown_fallback = await oracle._get_fallback_price("UNKNOWN")
    assert unknown_fallback == Decimal("0")
