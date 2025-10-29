"""
Tests for the logger module and terminal output formatting
"""
import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.logger import setup_logger, TerminalFormatter, TradingBotLogger


class TestTerminalFormatter:
    """Test TerminalFormatter class"""
    
    def test_success_formatting(self):
        """Test success message formatting"""
        result = TerminalFormatter.success("Test Success")
        assert "Test Success" in result
    
    def test_error_formatting(self):
        """Test error message formatting"""
        result = TerminalFormatter.error("Test Error")
        assert "Test Error" in result
    
    def test_format_price(self):
        """Test price formatting"""
        result = TerminalFormatter.format_price(1850.50)
        assert "1850.50" in result
    
    def test_format_profit_positive(self):
        """Test positive profit formatting"""
        result = TerminalFormatter.format_profit(100.50)
        assert "100.50" in result
    
    def test_format_profit_negative(self):
        """Test negative profit formatting"""
        result = TerminalFormatter.format_profit(-50.25)
        assert "50.25" in result
    
    def test_format_percentage_positive(self):
        """Test positive percentage formatting"""
        result = TerminalFormatter.format_percentage(0.3925)
        assert "0.3925" in result
    
    def test_separator(self):
        """Test separator creation"""
        result = TerminalFormatter.separator(50, "-")
        assert len(result) == 50
        assert result == "-" * 50


class TestTradingBotLogger:
    """Test TradingBotLogger class"""
    
    @pytest.fixture
    def logger(self, tmp_path):
        """Create a logger instance for testing"""
        log_file = tmp_path / "test.log"
        return setup_logger("TestBot", str(log_file), "DEBUG")
    
    def test_logger_creation(self, logger):
        """Test logger is created successfully"""
        assert logger is not None
        assert isinstance(logger, TradingBotLogger)
    
    def test_info_logging(self, logger):
        """Test info logging"""
        logger.info("Test info message")
        # If no exception, test passes
    
    def test_debug_logging(self, logger):
        """Test debug logging"""
        logger.debug("Test debug message")
    
    def test_warning_logging(self, logger):
        """Test warning logging"""
        logger.warning("Test warning message")
    
    def test_error_logging(self, logger):
        """Test error logging"""
        logger.error("Test error message")
    
    def test_success_logging(self, logger):
        """Test success logging"""
        logger.success("Test success message")
    
    def test_price_comparison_table(self, logger):
        """Test price comparison table display"""
        data = [
            {
                'source': 'Uniswap V3',
                'price': 1850.50,
                'liquidity': 500000.00,
                'spread': 0.0950
            },
            {
                'source': 'QuickSwap',
                'price': 1850.60,
                'liquidity': 450000.00,
                'spread': None
            }
        ]
        logger.print_price_comparison_table("POLYGON", "USDC/WETH", data)
    
    def test_execution_results(self, logger):
        """Test execution results display"""
        logger.print_execution_results(
            tx_hash="0x1a2b3c4d5e6f",
            block_number=45001234,
            gas_used=287456,
            exec_time=2.34,
            entry_price=1850.50,
            exit_price=1851.23,
            gross_profit=73.00,
            flash_fee=0.15,
            net_profit=72.85,
            roi=0.3925
        )
    
    def test_trading_statistics(self, logger):
        """Test trading statistics display"""
        logger.print_trading_statistics(
            total_trades=5,
            winning_trades=4,
            total_profit=342.15,
            total_loss=-28.50,
            net_profit=313.65
        )
    
    def test_cycle_header(self, logger):
        """Test cycle header display"""
        logger.print_cycle_header(1, "2024-10-29 14:23:45")
    
    def test_log_opportunity(self, logger):
        """Test opportunity logging"""
        logger.log_opportunity(
            "CROSS-CHAIN ARB",
            72.85,
            0.3925,
            rank=1
        )


def test_setup_logger(tmp_path):
    """Test logger setup function"""
    log_file = tmp_path / "test.log"
    logger = setup_logger("TestBot", str(log_file), "INFO")
    assert logger is not None
    assert isinstance(logger, TradingBotLogger)
