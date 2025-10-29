"""Base strategy class for trading strategies"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class BaseStrategy(ABC):
    """Abstract base class for trading strategies"""
    
    def __init__(self, name: str, logger):
        self.name = name
        self.logger = logger
        self.opportunities = []
    
    @abstractmethod
    async def scan_for_opportunities(self) -> List[Dict]:
        """
        Scan for trading opportunities
        
        Returns:
            List of opportunity dictionaries
        """
        pass
    
    @abstractmethod
    async def execute_opportunity(self, opportunity: Dict) -> Dict:
        """
        Execute a trading opportunity
        
        Args:
            opportunity: Opportunity dictionary
        
        Returns:
            Execution result dictionary
        """
        pass
    
    def calculate_profit(self, entry_price: float, exit_price: float, 
                        amount: float, fees: float = 0) -> Dict:
        """
        Calculate profit from a trade
        
        Args:
            entry_price: Entry price
            exit_price: Exit price
            amount: Trade amount
            fees: Total fees
        
        Returns:
            Dictionary with profit calculations
        """
        price_diff = exit_price - entry_price
        gross_profit = price_diff * amount
        net_profit = gross_profit - fees
        roi = (net_profit / (entry_price * amount)) * 100 if entry_price * amount > 0 else 0
        
        return {
            'price_difference': price_diff,
            'gross_profit': gross_profit,
            'net_profit': net_profit,
            'roi': roi
        }
