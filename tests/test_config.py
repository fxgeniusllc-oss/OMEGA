"""
Tests for configuration loading
"""
import os
import pytest
from src.config import Config

def test_config_loads_from_env(monkeypatch):
    """Test that configuration loads from environment variables"""
    # Set test environment variables
    monkeypatch.setenv('MODE', 'DEV')
    monkeypatch.setenv('BOT_ADDRESS', '0x1234567890123456789012345678901234567890')
    monkeypatch.setenv('POLYGON_ENABLED', 'true')
    monkeypatch.setenv('MIN_PROFIT_USD', '20')
    
    config = Config()
    
    assert config.mode == 'DEV'
    assert config.bot_address == '0x1234567890123456789012345678901234567890'
    assert 'POLYGON' in config.enabled_chains
    assert config.min_profit_usd == 20.0

def test_rpc_fallback_configuration(monkeypatch):
    """Test that RPC fallback is configured correctly"""
    monkeypatch.setenv('INFURA_POLYGON_RPC', 'https://polygon-infura.io')
    monkeypatch.setenv('QUICKNODE_RPC_URL', 'https://polygon-quicknode.io')
    monkeypatch.setenv('ALCHEMY_RPC_URL', 'https://polygon-alchemy.io')
    
    config = Config()
    
    polygon_rpcs = config.get_all_rpc_urls('POLYGON')
    assert len(polygon_rpcs) == 3
    assert 'infura' in polygon_rpcs[0]
    assert 'quicknode' in polygon_rpcs[1]
    assert 'alchemy' in polygon_rpcs[2]

def test_active_dexs_parsing(monkeypatch):
    """Test that active DEXs are parsed correctly"""
    monkeypatch.setenv('ACTIVE_DEXS', 'quickswap,uniswap_v3,sushiswap')
    
    config = Config()
    
    assert 'QUICKSWAP' in config.active_dexs
    assert 'UNISWAP_V3' in config.active_dexs
    assert 'SUSHISWAP' in config.active_dexs

def test_token_addresses_loaded(monkeypatch):
    """Test that token addresses are loaded"""
    monkeypatch.setenv('WMATIC', '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270')
    monkeypatch.setenv('USDC', '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174')
    
    config = Config()
    
    assert config.token_addresses['WMATIC'] == '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270'
    assert config.token_addresses['USDC'] == '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174'

def test_risk_management_settings(monkeypatch):
    """Test risk management settings"""
    monkeypatch.setenv('MIN_PROFIT_USD', '15')
    monkeypatch.setenv('MIN_LIQUIDITY_USD', '50000')
    monkeypatch.setenv('SLIPPAGE_BPS', '50')
    
    config = Config()
    
    assert config.min_profit_usd == 15.0
    assert config.min_liquidity_usd == 50000.0
    assert config.slippage_bps == 50
