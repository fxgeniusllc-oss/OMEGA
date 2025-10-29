"""
Cross-chain arbitrage strategy
"""
import asyncio
from typing import Dict, List
from decimal import Decimal
from .base import BaseStrategy

class CrossChainArbitrage(BaseStrategy):
    """Cross-chain arbitrage strategy"""
    
    def __init__(self, config, logger, blockchain, oracle):
        super().__init__("Cross-Chain Arbitrage", config, logger, blockchain, oracle)
        self.scan_interval = config.scan_cycle_interval_ms / 1000.0
    
    async def scan(self) -> List[Dict]:
        """Scan for cross-chain arbitrage opportunities"""
        opportunities = []
        
        if not self.enabled:
            return opportunities
        
        # Get enabled chains
        chains = self.config.enabled_chains
        
        if len(chains) < 2:
            # Need at least 2 chains for cross-chain arbitrage
            return opportunities
        
        # Scan each token across chains
        for token_symbol, token_address in self.config.token_addresses.items():
            if not token_address:
                continue
            
            try:
                # Get prices on different chains/DEXs
                prices = await self._get_token_prices_across_chains(token_symbol)
                
                # Find arbitrage opportunities
                arb_opps = self._find_arbitrage_opportunities(token_symbol, prices)
                opportunities.extend(arb_opps)
                
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error scanning {token_symbol}: {e}")
        
        return opportunities
    
    async def _get_token_prices_across_chains(self, token_symbol: str) -> Dict:
        """Get token prices across all enabled chains and DEXs"""
        prices = {}
        
        for chain in self.config.enabled_chains:
            prices[chain] = {}
            
            for dex in self.config.active_dexs:
                # Simulate price fetching (in real implementation, query DEX contracts)
                try:
                    price = await self._fetch_dex_price(chain, dex, token_symbol)
                    if price:
                        prices[chain][dex] = price
                except Exception as e:
                    if self.logger:
                        self.logger.debug(f"Could not fetch {token_symbol} price from {dex} on {chain}: {e}")
        
        return prices
    
    async def _fetch_dex_price(self, chain: str, dex: str, token_symbol: str) -> float:
        """Fetch token price from a specific DEX (simulated)"""
        # In a real implementation, this would:
        # 1. Get the DEX router contract
        # 2. Query the pool reserves
        # 3. Calculate the price
        
        # For now, return base price with some variation
        base_price = await self.oracle.get_price(token_symbol)
        
        # Add some random variation to simulate different DEX prices
        import random
        variation = random.uniform(-0.02, 0.02)  # +/- 2%
        return base_price * (1 + variation)
    
    def _find_arbitrage_opportunities(self, token_symbol: str, prices: Dict) -> List[Dict]:
        """Find arbitrage opportunities from price data"""
        opportunities = []
        
        # Find min and max prices
        all_prices = []
        for chain, dex_prices in prices.items():
            for dex, price in dex_prices.items():
                all_prices.append({
                    'chain': chain,
                    'dex': dex,
                    'price': price
                })
        
        if len(all_prices) < 2:
            return opportunities
        
        # Sort by price
        all_prices.sort(key=lambda x: x['price'])
        
        # Calculate potential profit
        buy_at = all_prices[0]
        sell_at = all_prices[-1]
        
        price_diff = sell_at['price'] - buy_at['price']
        profit_percent = (price_diff / buy_at['price']) * 100
        
        # Estimate profit in USD (using example trade size)
        trade_size_usd = self.config.min_trade_size_usd
        estimated_profit_usd = trade_size_usd * (profit_percent / 100)
        
        # Check if profitable after gas costs (simplified)
        gas_cost_usd = 10  # Simplified gas estimate
        net_profit_usd = estimated_profit_usd - gas_cost_usd
        
        if self.is_profitable(net_profit_usd):
            opportunity = {
                'strategy': self.name,
                'token': token_symbol,
                'buy_chain': buy_at['chain'],
                'buy_dex': buy_at['dex'],
                'buy_price': buy_at['price'],
                'sell_chain': sell_at['chain'],
                'sell_dex': sell_at['dex'],
                'sell_price': sell_at['price'],
                'profit_usd': net_profit_usd,
                'profit_percent': profit_percent,
                'confidence': min(0.95, 0.5 + (profit_percent / 10)),
                'chain': buy_at['chain'],
                'dex_pair': f"{buy_at['dex']} → {sell_at['dex']}"
            }
            
            opportunities.append(opportunity)
            self.log_opportunity(opportunity)
        
        return opportunities
    
    async def execute(self, opportunity: Dict) -> bool:
        """Execute cross-chain arbitrage trade"""
        if not self.config.live_execution:
            # Simulation mode
            if self.logger:
                self.logger.info(f"📝 [SIMULATION] Would execute: {opportunity['token']} arbitrage")
                self.logger.info(f"   Buy on {opportunity['buy_chain']}:{opportunity['buy_dex']} @ ${opportunity['buy_price']:.4f}")
                self.logger.info(f"   Sell on {opportunity['sell_chain']}:{opportunity['sell_dex']} @ ${opportunity['sell_price']:.4f}")
                self.logger.info(f"   Expected profit: ${opportunity['profit_usd']:.2f}")
            
            # Log as executed trade
            trade_data = {
                'strategy': self.name,
                'dex': opportunity['dex_pair'],
                'profit_usd': opportunity['profit_usd'],
                'token': opportunity['token'],
                'amount': self.config.min_trade_size_usd / opportunity['buy_price']
            }
            self.log_trade(trade_data)
            
            return True
        
        # Real execution would happen here
        # 1. Get flash loan
        # 2. Buy on source chain/DEX
        # 3. Bridge to target chain
        # 4. Sell on target chain/DEX
        # 5. Repay flash loan + keep profit
        
        if self.logger:
            self.logger.warning("Live execution not fully implemented")
        
        return False
