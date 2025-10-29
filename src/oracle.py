"""
Price oracle for USD conversions and price feeds
"""
import asyncio
import aiohttp
from typing import Dict, Optional
from decimal import Decimal
from .utils.constants import TOKEN_DECIMALS

class PriceOracle:
    """Price oracle for fetching and caching token prices in USD"""
    
    def __init__(self, coingecko_api_key: Optional[str] = None):
        self.coingecko_api_key = coingecko_api_key
        self.price_cache: Dict[str, float] = {}
        self.cache_duration = 60  # Cache prices for 60 seconds
        
        # Default prices for common tokens (used as fallback)
        self.fallback_prices = {
            'WMATIC': 0.85,
            'MATIC': 0.85,
            'ETH': 3000.0,
            'WETH': 3000.0,
            'USDC': 1.0,
            'USDT': 1.0,
            'DAI': 1.0,
            'WBTC': 60000.0,
            'BTC': 60000.0,
            'LINK': 15.0,
            'AAVE': 100.0,
            'UNI': 8.0,
        }
        
        # CoinGecko ID mapping
        self.coingecko_ids = {
            'WMATIC': 'matic-network',
            'MATIC': 'matic-network',
            'ETH': 'ethereum',
            'WETH': 'ethereum',
            'USDC': 'usd-coin',
            'USDT': 'tether',
            'DAI': 'dai',
            'WBTC': 'wrapped-bitcoin',
            'BTC': 'bitcoin',
            'LINK': 'chainlink',
            'AAVE': 'aave',
            'UNI': 'uniswap',
        }
    
    async def get_price(self, token_symbol: str) -> float:
        """Get token price in USD"""
        token_symbol = token_symbol.upper()
        
        # Check cache first
        if token_symbol in self.price_cache:
            return self.price_cache[token_symbol]
        
        # Try to fetch from CoinGecko
        try:
            price = await self._fetch_from_coingecko(token_symbol)
            if price:
                self.price_cache[token_symbol] = price
                return price
        except Exception as e:
            print(f"Error fetching price for {token_symbol}: {e}")
        
        # Fallback to cached/default prices
        if token_symbol in self.fallback_prices:
            return self.fallback_prices[token_symbol]
        
        return 0.0
    
    async def _fetch_from_coingecko(self, token_symbol: str) -> Optional[float]:
        """Fetch price from CoinGecko API"""
        if token_symbol not in self.coingecko_ids:
            return None
        
        coin_id = self.coingecko_ids[token_symbol]
        url = f"https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': coin_id,
            'vs_currencies': 'usd'
        }
        
        headers = {}
        if self.coingecko_api_key:
            headers['X-Cg-Pro-Api-Key'] = self.coingecko_api_key
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, headers=headers, timeout=5) as response:
                    if response.status == 200:
                        data = await response.json()
                        if coin_id in data and 'usd' in data[coin_id]:
                            return float(data[coin_id]['usd'])
        except Exception:
            pass
        
        return None
    
    def get_price_sync(self, token_symbol: str) -> float:
        """Synchronous wrapper for get_price"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If loop is already running, return fallback
                return self.fallback_prices.get(token_symbol.upper(), 0.0)
            else:
                return loop.run_until_complete(self.get_price(token_symbol))
        except Exception:
            return self.fallback_prices.get(token_symbol.upper(), 0.0)
    
    def token_amount_to_usd(self, amount: float, token_symbol: str, decimals: Optional[int] = None) -> float:
        """Convert token amount to USD"""
        if decimals is None:
            decimals = TOKEN_DECIMALS.get(token_symbol.upper(), 18)
        
        # Convert from wei/smallest unit to token amount
        token_amount = amount / (10 ** decimals)
        
        # Get price and convert to USD
        price = self.get_price_sync(token_symbol)
        return token_amount * price
    
    def usd_to_token_amount(self, usd_amount: float, token_symbol: str, decimals: Optional[int] = None) -> int:
        """Convert USD amount to token amount (in wei/smallest unit)"""
        if decimals is None:
            decimals = TOKEN_DECIMALS.get(token_symbol.upper(), 18)
        
        price = self.get_price_sync(token_symbol)
        if price == 0:
            return 0
        
        # Calculate token amount
        token_amount = usd_amount / price
        
        # Convert to wei/smallest unit
        return int(token_amount * (10 ** decimals))
    
    def update_fallback_price(self, token_symbol: str, price: float):
        """Update fallback price for a token"""
        self.fallback_prices[token_symbol.upper()] = price
    
    def clear_cache(self):
        """Clear price cache"""
        self.price_cache.clear()
    
    def get_all_prices(self) -> Dict[str, float]:
        """Get all current prices (cached + fallback)"""
        all_prices = self.fallback_prices.copy()
        all_prices.update(self.price_cache)
        return all_prices
