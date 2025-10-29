"""Base strategy class."""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import asyncio


class BaseStrategy(ABC):
    """Base class for all trading strategies."""
    
    def __init__(self, name: str, config, blockchain, oracle, logger):
        """
        Initialize base strategy.
        
        Args:
            name: Strategy name
            config: Configuration object
            blockchain: Blockchain interface
            oracle: Price oracle
            logger: Logger instance
        """
        self.name = name
        self.config = config
        self.blockchain = blockchain
        self.oracle = oracle
        self.logger = logger
        self.enabled = True
        self.opportunities_found = 0
        self.trades_executed = 0
    
    @abstractmethod
    async def scan_opportunities(self) -> List[Dict]:
        """
        Scan for trading opportunities.
        
        Returns:
            List of opportunity dictionaries
        """
        pass
    
    @abstractmethod
    async def execute_opportunity(self, opportunity: Dict) -> bool:
        """
        Execute a trading opportunity.
        
        Args:
            opportunity: Opportunity dictionary
        
        Returns:
            True if execution successful
        """
        pass
    
    async def run(self) -> List[Dict]:
        """
        Run the strategy (scan and return opportunities).
        
        Returns:
            List of opportunities found
        """
        if not self.enabled:
            return []
        
        try:
            opportunities = await self.scan_opportunities()
            self.opportunities_found += len(opportunities)
            
            if opportunities:
                self.logger.info(
                    f"{self.name}: Found {len(opportunities)} opportunities"
                )
            
            return opportunities
        except Exception as e:
            self.logger.error(f"{self.name} error: {e}")
            return []
    
    def enable(self):
        """Enable the strategy."""
        self.enabled = True
        self.logger.info(f"{self.name} enabled")
    
    def disable(self):
        """Disable the strategy."""
        self.enabled = False
        self.logger.info(f"{self.name} disabled")
    
    def get_stats(self) -> Dict:
        """Get strategy statistics."""
        return {
            'name': self.name,
            'enabled': self.enabled,
            'opportunities_found': self.opportunities_found,
            'trades_executed': self.trades_executed,
        }
