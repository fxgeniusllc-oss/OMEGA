"""
Tests for the configuration module
"""
import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config import Config


class TestConfig:
    """Test Config class"""
    
    def test_mode_default(self):
        """Test MODE has a default value"""
        assert Config.MODE is not None
    
    def test_get_active_strategies(self):
        """Test get_active_strategies method"""
        strategies = Config.get_active_strategies()
        assert isinstance(strategies, list)
    
    def test_get_active_dexs(self):
        """Test get_active_dexs method"""
        dexs = Config.get_active_dexs()
        assert isinstance(dexs, list)
    
    def test_is_simulation_mode(self):
        """Test is_simulation_mode method"""
        result = Config.is_simulation_mode()
        assert isinstance(result, bool)
    
    def test_min_profit_usd(self):
        """Test MIN_PROFIT_USD is a float"""
        assert isinstance(Config.MIN_PROFIT_USD, float)
    
    def test_min_liquidity_usd(self):
        """Test MIN_LIQUIDITY_USD is a float"""
        assert isinstance(Config.MIN_LIQUIDITY_USD, float)
    
    def test_scan_cycle_interval_ms(self):
        """Test SCAN_CYCLE_INTERVAL_MS is an int"""
        assert isinstance(Config.SCAN_CYCLE_INTERVAL_MS, int)
    
    def test_log_level(self):
        """Test LOG_LEVEL has a value"""
        assert Config.LOG_LEVEL is not None
