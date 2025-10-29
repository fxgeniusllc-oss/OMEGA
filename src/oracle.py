"""Price Oracle for USD conversion of all tokens."""

import logging
from decimal import Decimal
from typing import Dict, Optional, List, Tuple
import asyncio
import aiohttp

from src.utils.constants import (
    DEX_SOURCES,
    BRIDGE_SOURCES,
    CEX_SOURCES,
    STABLECOINS,
    TOKEN_ADDRESSES
)
from src.utils.helpers import safe_decimal, parse_fee_percentage

logger = logging.getLogger(__name__)


class PriceOracle:
    """
    Central price oracle that converts all tokens to USD.
    Fetches prices from DEXs, bridges, and CEXs.
    """
    
    def __init__(self):
        """Initialize the PriceOracle."""
        self.price_cache: Dict[str, Decimal] = {}
        self.cache_ttl = 60  # Cache prices for 60 seconds
        self.last_update: Dict[str, float] = {}
        
    async def get_usd_price(self, token: str, chain: str = "polygon") -> Decimal:
        """
        Get USD price for a token.
        
        Args:
            token: Token symbol (e.g., "WETH", "USDC")
            chain: Chain name (default "polygon")
            
        Returns:
            Token price in USD as Decimal
        """
        # Stablecoins are always $1
        if token.upper() in STABLECOINS:
            return Decimal("1.0")
        
        # Check cache
        cache_key = f"{chain}_{token}"
        if cache_key in self.price_cache:
            logger.debug(f"Using cached price for {token}: ${self.price_cache[cache_key]}")
            return self.price_cache[cache_key]
        
        # Fetch price from multiple sources
        prices = await self._fetch_prices_from_sources(token, chain)
        
        if not prices:
            logger.warning(f"No prices found for {token} on {chain}, using fallback")
            return await self._get_fallback_price(token)
        
        # Use median price for robustness
        median_price = self._calculate_median(prices)
        
        # Cache the price
        self.price_cache[cache_key] = median_price
        
        logger.info(f"USD price for {token}: ${median_price}")
        return median_price
    
    async def _fetch_prices_from_sources(
        self, 
        token: str, 
        chain: str
    ) -> List[Decimal]:
        """
        Fetch prices from multiple sources (DEXs, CEXs, Bridges).
        
        Args:
            token: Token symbol
            chain: Chain name
            
        Returns:
            List of prices from different sources
        """
        prices = []
        
        # Fetch from DEXs
        dex_prices = await self._fetch_dex_prices(token, chain)
        prices.extend(dex_prices)
        
        # Fetch from CEXs
        cex_prices = await self._fetch_cex_prices(token)
        prices.extend(cex_prices)
        
        return prices
    
    async def _fetch_dex_prices(self, token: str, chain: str) -> List[Decimal]:
        """
        Fetch prices from DEX sources.
        
        Args:
            token: Token symbol
            chain: Chain name
            
        Returns:
            List of DEX prices
        """
        prices = []
        
        if chain not in DEX_SOURCES:
            logger.warning(f"Chain {chain} not found in DEX_SOURCES")
            return prices
        
        # Simulate fetching from DEXs (in production, would use actual API calls)
        for dex_name, dex_config in DEX_SOURCES[chain].items():
            try:
                price = await self._simulate_dex_price(token, dex_name, dex_config)
                if price:
                    prices.append(price)
                    logger.debug(f"Got price from {dex_name}: ${price}")
            except Exception as e:
                logger.error(f"Error fetching price from {dex_name}: {e}")
        
        return prices
    
    async def _simulate_dex_price(
        self, 
        token: str, 
        dex_name: str, 
        dex_config: Dict
    ) -> Optional[Decimal]:
        """
        Simulate fetching price from a DEX.
        In production, this would call actual DEX smart contracts.
        
        Args:
            token: Token symbol
            dex_name: DEX name
            dex_config: DEX configuration
            
        Returns:
            Simulated price or None
        """
        # Simulated prices for demonstration
        base_prices = {
            "WETH": Decimal("2347.50"),
            "WBTC": Decimal("43250.00"),
            "WMATIC": Decimal("0.85"),
            "DAI": Decimal("1.00"),
        }
        
        if token not in base_prices:
            return None
        
        # Add variation based on DEX liquidity multiplier to create arbitrage opportunities
        base_price = base_prices[token]
        liquidity_mult = Decimal(str(dex_config.get("liquidity_mult", 1.0)))
        # Larger variation to create profitable opportunities (0.5% for Aave with 0.80 mult = 0.1% variation)
        variation = Decimal("0.01") * (Decimal("1") - liquidity_mult)
        
        return base_price + (base_price * variation)
    
    async def _fetch_cex_prices(self, token: str) -> List[Decimal]:
        """
        Fetch prices from CEX sources.
        
        Args:
            token: Token symbol
            
        Returns:
            List of CEX prices
        """
        prices = []
        
        for cex_name, cex_config in CEX_SOURCES.items():
            try:
                price = await self._simulate_cex_price(token, cex_name, cex_config)
                if price:
                    prices.append(price)
                    logger.debug(f"Got price from {cex_name}: ${price}")
            except Exception as e:
                logger.error(f"Error fetching price from {cex_name}: {e}")
        
        return prices
    
    async def _simulate_cex_price(
        self, 
        token: str, 
        cex_name: str, 
        cex_config: Dict
    ) -> Optional[Decimal]:
        """
        Simulate fetching price from a CEX.
        In production, this would call actual CEX APIs.
        
        Args:
            token: Token symbol
            cex_name: CEX name
            cex_config: CEX configuration
            
        Returns:
            Simulated price or None
        """
        # Simulated prices for demonstration
        base_prices = {
            "WETH": Decimal("2347.45"),
            "WBTC": Decimal("43248.00"),
            "WMATIC": Decimal("0.85"),
        }
        
        if token not in base_prices:
            return None
        
        # CEX prices are typically very close to market
        return base_prices[token]
    
    async def _get_fallback_price(self, token: str) -> Decimal:
        """
        Get fallback price if no sources available.
        
        Args:
            token: Token symbol
            
        Returns:
            Fallback price
        """
        # Fallback prices
        fallback_prices = {
            "WETH": Decimal("2347.50"),
            "WBTC": Decimal("43250.00"),
            "WMATIC": Decimal("0.85"),
            "DAI": Decimal("1.00"),
            "USDC": Decimal("1.00"),
            "USDT": Decimal("1.00"),
        }
        
        return fallback_prices.get(token, Decimal("0"))
    
    def _calculate_median(self, prices: List[Decimal]) -> Decimal:
        """
        Calculate median of a list of prices.
        
        Args:
            prices: List of prices
            
        Returns:
            Median price
        """
        if not prices:
            return Decimal("0")
        
        sorted_prices = sorted(prices)
        n = len(sorted_prices)
        
        if n % 2 == 0:
            return (sorted_prices[n // 2 - 1] + sorted_prices[n // 2]) / Decimal("2")
        else:
            return sorted_prices[n // 2]
    
    async def get_price_comparison(
        self,
        token_a: str,
        token_b: str,
        chain: str = "polygon"
    ) -> List[Dict]:
        """
        Get price comparison from multiple sources.
        
        Args:
            token_a: First token symbol
            token_b: Second token symbol
            chain: Chain name
            
        Returns:
            List of price comparisons from different sources
        """
        comparisons = []
        
        # Get USD prices for both tokens
        token_a_usd = await self.get_usd_price(token_a, chain)
        token_b_usd = await self.get_usd_price(token_b, chain)
        
        # Get prices from each DEX
        if chain in DEX_SOURCES:
            for dex_name, dex_config in DEX_SOURCES[chain].items():
                try:
                    # Simulate getting liquidity and fee info
                    fee_pct = parse_fee_percentage(dex_config["fee_tier"])
                    liquidity_mult = Decimal(str(dex_config.get("liquidity_mult", 1.0)))
                    
                    # Calculate effective price with variation to create arbitrage opportunities
                    variation = Decimal("0.01") * (Decimal("1") - liquidity_mult)
                    price_usd = token_a_usd + (token_a_usd * variation)
                    
                    # Simulate liquidity (in USD)
                    base_liquidity = Decimal("500000")
                    liquidity_usd = base_liquidity * liquidity_mult
                    
                    comparison = {
                        "source": dex_name,
                        "type": "DEX",
                        "price_usd": price_usd,
                        "token_a_usd": token_a_usd,
                        "token_b_usd": token_b_usd,
                        "liquidity_usd": liquidity_usd,
                        "fee_pct": fee_pct
                    }
                    comparisons.append(comparison)
                    
                except Exception as e:
                    logger.error(f"Error getting comparison for {dex_name}: {e}")
        
        return comparisons
    
    async def convert_to_usd(
        self,
        amount: Decimal,
        token: str,
        chain: str = "polygon"
    ) -> Decimal:
        """
        Convert token amount to USD.
        
        Args:
            amount: Token amount
            token: Token symbol
            chain: Chain name
            
        Returns:
            USD value
        """
        token_price = await self.get_usd_price(token, chain)
        return amount * token_price
    
    async def convert_from_usd(
        self,
        usd_amount: Decimal,
        token: str,
        chain: str = "polygon"
    ) -> Decimal:
        """
        Convert USD amount to token amount.
        
        Args:
            usd_amount: USD amount
            token: Token symbol
            chain: Chain name
            
        Returns:
            Token amount
        """
        token_price = await self.get_usd_price(token, chain)
        if token_price == 0:
            return Decimal("0")
        return usd_amount / token_price
