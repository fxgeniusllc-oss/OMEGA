"""
Test suite for the trading bot.
"""

import pytest
import os
from dotenv import load_dotenv


def test_env_example_exists():
    """Test that .env.example exists"""
    assert os.path.exists('.env.example'), ".env.example file should exist"


def test_requirements_exists():
    """Test that requirements.txt exists"""
    assert os.path.exists('requirements.txt'), "requirements.txt file should exist"


def test_bot_module_import():
    """Test that bot module can be imported"""
    try:
        from src.bot import UnifiedTradingBot
        assert UnifiedTradingBot is not None
    except ImportError as e:
        pytest.fail(f"Failed to import bot module: {e}")


def test_env_loading():
    """Test that environment variables can be loaded"""
    load_dotenv('.env.example')
    mode = os.getenv('MODE')
    assert mode is not None, "MODE environment variable should be set"
    assert mode == 'DEV', "Default MODE should be DEV"


def test_directory_structure():
    """Test that required directories exist"""
    required_dirs = ['src', 'src/strategies', 'src/utils', 'tests', 'scripts', 'docker', 'logs', 'models']
    for dir_path in required_dirs:
        assert os.path.isdir(dir_path), f"Directory {dir_path} should exist"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
