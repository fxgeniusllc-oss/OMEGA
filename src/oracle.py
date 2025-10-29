"""Price oracle and conversion utilities."""
import asyncio
import aiohttp
from typing import Dict, Optional
from datetime import datetime, timedelta


class PriceOracle:
    """Handles price feeds and conversions."""
    
    def __init__(self):
        """Initialize price oracle."""
        self._price_cache: Dict[str, tuple] = {}  # (price, timestamp)
        self._cache_duration = timedelta(seconds=30)
    
    async def get_price(self, token_symbol: str, quote_currency: str = "USD") -> Optional[float]:
        """Get price for a token."""
        cache_key = f"{token_symbol}_{quote_currency}"
        
        # Check cache
        if cache_key in self._price_cache:
            price, timestamp = self._price_cache[cache_key]
            if datetime.now() - timestamp < self._cache_duration:
                return price
        
        # Fetch from API (mock implementation)
        price = await self._fetch_price_from_api(token_symbol, quote_currency)
        
        if price:
            self._price_cache[cache_key] = (price, datetime.now())
        
        return price
    
    async def _fetch_price_from_api(self, token_symbol: str, quote_currency: str) -> Optional[float]:
        """Fetch price from external API."""
        # Mock prices for simulation
        mock_prices = {
            "MATIC_USD": 0.85,
            "ETH_USD": 2000.0,
            "BTC_USD": 42000.0,
            "USDC_USD": 1.0,
            "USDT_USD": 1.0,
            "DAI_USD": 1.0,
        }
        
        key = f"{token_symbol}_{quote_currency}"
        return mock_prices.get(key)
    
    async def convert_amount(self, amount: float, from_token: str, to_token: str) -> Optional[float]:
        """Convert amount from one token to another."""
        if from_token == to_token:
            return amount
        
        from_price = await self.get_price(from_token, "USD")
        to_price = await self.get_price(to_token, "USD")
        
        if from_price and to_price and to_price > 0:
            return (amount * from_price) / to_price
        
        return None
    
    async def get_token_price_usd(self, token_address: str, chain: str = "POLYGON") -> Optional[float]:
        """Get USD price for a token by address."""
        # Mock implementation - would query DEX or price feed
        token_map = {
            "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270": "MATIC",
            "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619": "ETH",
            "0x1BFD67037B42Cf73acF2047067bd4F2C47D9BfD6": "BTC",
            "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174": "USDC",
            "0xc2132D05D31c914a87C6611C10748AEb04B58e8F": "USDT",
            "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063": "DAI",
        }
        
        token_symbol = token_map.get(token_address.lower())
        if token_symbol:
            return await self.get_price(token_symbol, "USD")
        
        return None
