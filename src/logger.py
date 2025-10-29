"""Enhanced logging setup for the DeFi Trading Bot."""

import logging
import sys
from pathlib import Path


def setup_logger(
    name: str = "TradingBot",
    log_file: str = "trading_bot.log",
    log_level: str = "INFO"
) -> logging.Logger:
    """
    Setup enhanced logger with console and file output.
    
    Args:
        name: Logger name
        log_file: Log file path
        log_level: Logging level
        
    Returns:
        Configured logger
    """
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers
    logger.handlers = []
    
    # Console handler with formatting
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # File handler with detailed formatting
    if log_file:
        file_handler = logging.FileHandler(log_dir / log_file)
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
    
    return logger


def log_price_comparison_table(comparisons: list, token_a: str, token_b: str, chain: str):
    """
    Log a formatted price comparison table.
    
    Args:
        comparisons: List of price comparisons
        token_a: First token symbol
        token_b: Second token symbol
        chain: Chain name
    """
    logger = logging.getLogger("TradingBot")
    
    # Header
    separator = "=" * 125
    logger.info(separator)
    logger.info(f"PRICE COMPARISON - {chain.upper()} | {token_a}/{token_b} (ALL VALUES IN USD)")
    logger.info(separator)
    
    # Column headers
    header = f"{'Source':<20} {'Type':<10} {'Price USD':<20} {'Token A USD':<20} {'Token B USD':<20} {'Liquidity USD':<20} {'Fee%':<10}"
    logger.info(header)
    logger.info("-" * 125)
    
    # Data rows
    from src.utils.helpers import format_usd
    
    for comp in comparisons:
        source = comp["source"]
        type_ = comp["type"]
        price_usd = format_usd(comp["price_usd"], 8)
        token_a_usd = format_usd(comp["token_a_usd"], 8)
        token_b_usd = format_usd(comp["token_b_usd"], 8)
        liquidity_usd = format_usd(comp["liquidity_usd"], 2)
        fee_pct = f"{comp['fee_pct'] * 100:.4f}"
        
        row = f"{source:<20} {type_:<10} {price_usd:<20} {token_a_usd:<20} {token_b_usd:<20} {liquidity_usd:<20} {fee_pct:<10}"
        logger.info(row)
    
    # Footer with statistics
    logger.info(separator)
    
    if comparisons:
        from decimal import Decimal
        prices = [comp["price_usd"] for comp in comparisons]
        min_price = min(prices)
        max_price = max(prices)
        spread = ((max_price - min_price) / min_price) * Decimal("100")
        
        logger.info(f"Price Range: {format_usd(min_price)} - {format_usd(max_price)} | Spread: {spread:.4f}%")
        logger.info(f"Total Sources Analyzed: {len(comparisons)}")
    
    logger.info(separator)


def log_execution_results(results: dict):
    """
    Log execution results with profitability in USD.
    
    Args:
        results: Dictionary containing execution results
    """
    logger = logging.getLogger("TradingBot")
    from src.utils.helpers import format_usd
    
    logger.info("\nPROFITABILITY (ALL IN USD):")
    logger.info(f"  Gross Profit: {format_usd(results.get('gross_profit', 0))}")
    logger.info(f"  Flash Loan Fee: -{format_usd(results.get('flash_loan_fee', 0))}")
    logger.info(f"  Bridge Fee: -{format_usd(results.get('bridge_fee', 0))}")
    logger.info(f"  Gas Cost: -{format_usd(results.get('gas_cost', 0))}")
    logger.info(f"  Total Fees: -{format_usd(results.get('total_fees', 0))}")
    logger.info(f"  Net Profit (USD): {format_usd(results.get('net_profit', 0))}")
    logger.info(f"  ROI: {results.get('roi', 0):.4f}%")
