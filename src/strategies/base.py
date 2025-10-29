"""
Base strategy class for all trading strategies
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from decimal import Decimal

class BaseStrategy(ABC):
    """Base class for all trading strategies"""
    
    def __init__(self, name: str, config, logger, blockchain, oracle):
        self.name = name
        self.config = config
        self.logger = logger
        self.blockchain = blockchain
        self.oracle = oracle
        self.enabled = True
        self.opportunities_found = 0
        self.trades_executed = 0
    
    @abstractmethod
    async def scan(self) -> List[Dict]:
        """Scan for opportunities. Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    async def execute(self, opportunity: Dict) -> bool:
        """Execute a trade. Must be implemented by subclasses."""
        pass
    
    def is_profitable(self, profit_usd: float) -> bool:
        """Check if opportunity meets minimum profit threshold"""
        return profit_usd >= self.config.min_profit_usd
    
    def has_sufficient_liquidity(self, liquidity_usd: float) -> bool:
        """Check if pool has sufficient liquidity"""
        return liquidity_usd >= self.config.min_liquidity_usd
    
    def calculate_slippage_amount(self, amount: Decimal) -> Decimal:
        """Calculate slippage amount"""
        from ..utils.helpers import calculate_slippage
        return calculate_slippage(amount, self.config.slippage_bps)
    
    def log_opportunity(self, opportunity: Dict):
        """Log an opportunity"""
        self.opportunities_found += 1
        if self.logger:
            self.logger.log_opportunity(opportunity)
    
    def log_trade(self, trade_data: Dict):
        """Log a trade"""
        self.trades_executed += 1
        if self.logger:
            self.logger.log_trade(trade_data)
    
    def get_stats(self) -> Dict:
        """Get strategy statistics"""
        return {
            'name': self.name,
            'enabled': self.enabled,
            'opportunities_found': self.opportunities_found,
            'trades_executed': self.trades_executed,
        }
    
    def enable(self):
        """Enable strategy"""
        self.enabled = True
        if self.logger:
            self.logger.info(f"✓ {self.name} strategy enabled")
    
    def disable(self):
        """Disable strategy"""
        self.enabled = False
        if self.logger:
            self.logger.warning(f"✗ {self.name} strategy disabled")
