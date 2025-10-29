"""
Tests for strategy classes
"""
import pytest
import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.strategies.base import BaseStrategy
from src.strategies.arbitrage import CrossChainArbitrageStrategy, BridgeArbitrageStrategy
from src.logger import setup_logger


class TestBaseStrategy:
    """Test BaseStrategy class"""
    
    def test_calculate_profit(self):
        """Test profit calculation"""
        # Create a mock logger
        logger = setup_logger("TestBot", "test.log", "INFO")
        
        # Create a concrete implementation for testing
        class MockStrategy(BaseStrategy):
            async def scan_for_opportunities(self):
                return []
            
            async def execute_opportunity(self, opportunity):
                return {}
        
        strategy = MockStrategy("TEST", logger)
        
        result = strategy.calculate_profit(
            entry_price=1850.50,
            exit_price=1851.23,
            amount=100,
            fees=0.15
        )
        
        assert 'price_difference' in result
        assert 'gross_profit' in result
        assert 'net_profit' in result
        assert 'roi' in result
        assert result['price_difference'] == pytest.approx(0.73, rel=0.01)


class TestCrossChainArbitrageStrategy:
    """Test CrossChainArbitrageStrategy class"""
    
    @pytest.fixture
    def strategy(self, tmp_path):
        """Create strategy instance"""
        log_file = tmp_path / "test.log"
        logger = setup_logger("TestBot", str(log_file), "INFO")
        return CrossChainArbitrageStrategy(logger, min_profit_usd=15)
    
    def test_strategy_creation(self, strategy):
        """Test strategy is created successfully"""
        assert strategy is not None
        assert strategy.name == "CROSS-CHAIN ARB"
    
    @pytest.mark.asyncio
    async def test_scan_for_opportunities(self, strategy):
        """Test scanning for opportunities"""
        opportunities = await strategy.scan_for_opportunities()
        assert isinstance(opportunities, list)
    
    @pytest.mark.asyncio
    async def test_execute_opportunity(self, strategy):
        """Test executing an opportunity"""
        opportunity = {
            'strategy': 'CROSS-CHAIN ARB',
            'entry_price': 1850.50,
            'exit_price': 1851.23,
            'expected_profit': 72.85,
            'roi': 0.3925,
            'gas_estimate': 287456
        }
        
        result = await strategy.execute_opportunity(opportunity)
        assert isinstance(result, dict)
        assert 'success' in result


class TestBridgeArbitrageStrategy:
    """Test BridgeArbitrageStrategy class"""
    
    @pytest.fixture
    def strategy(self, tmp_path):
        """Create strategy instance"""
        log_file = tmp_path / "test.log"
        logger = setup_logger("TestBot", str(log_file), "INFO")
        return BridgeArbitrageStrategy(logger, min_profit_usd=15)
    
    def test_strategy_creation(self, strategy):
        """Test strategy is created successfully"""
        assert strategy is not None
        assert strategy.name == "BRIDGE ARBITRAGE"
    
    @pytest.mark.asyncio
    async def test_scan_for_opportunities(self, strategy):
        """Test scanning for opportunities"""
        opportunities = await strategy.scan_for_opportunities()
        assert isinstance(opportunities, list)
    
    @pytest.mark.asyncio
    async def test_execute_opportunity(self, strategy):
        """Test executing an opportunity"""
        opportunity = {
            'strategy': 'BRIDGE ARBITRAGE',
            'entry_price': 1.0000,
            'exit_price': 1.0015,
            'expected_profit': 45.50,
            'roi': 0.15,
            'gas_estimate': 150000
        }
        
        result = await strategy.execute_opportunity(opportunity)
        assert isinstance(result, dict)
        assert 'success' in result
