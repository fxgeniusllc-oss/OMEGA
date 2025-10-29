"""
Enhanced logging module with colored console output and file logging.
Supports color-coded messages for different types of information.
"""
import logging
import colorlog
from colorama import init, Fore, Back, Style
import os
from datetime import datetime

# Initialize colorama for Windows support
init(autoreset=True)


class ColorCodes:
    """ANSI color codes for terminal output"""
    GREEN = Fore.GREEN
    RED = Fore.RED
    BLUE = Fore.BLUE
    CYAN = Fore.CYAN
    YELLOW = Fore.YELLOW
    MAGENTA = Fore.MAGENTA
    WHITE = Fore.WHITE
    RESET = Style.RESET_ALL
    BOLD = Style.BRIGHT
    DIM = Style.DIM


class TerminalFormatter:
    """Formats terminal output with colors and styling"""
    
    @staticmethod
    def success(message):
        """Green for successes, profits"""
        return f"{ColorCodes.GREEN}{message}{ColorCodes.RESET}"
    
    @staticmethod
    def error(message):
        """Red for errors, losses"""
        return f"{ColorCodes.RED}{message}{ColorCodes.RESET}"
    
    @staticmethod
    def info(message):
        """Blue for transaction hashes, blockchain events"""
        return f"{ColorCodes.BLUE}{message}{ColorCodes.RESET}"
    
    @staticmethod
    def debug(message):
        """Cyan for price data, debug info"""
        return f"{ColorCodes.CYAN}{message}{ColorCodes.RESET}"
    
    @staticmethod
    def warning(message):
        """Yellow for warnings"""
        return f"{ColorCodes.YELLOW}{message}{ColorCodes.RESET}"
    
    @staticmethod
    def header(message):
        """Bold white for headers"""
        return f"{ColorCodes.BOLD}{ColorCodes.WHITE}{message}{ColorCodes.RESET}"
    
    @staticmethod
    def separator(width=80, char="="):
        """Create a separator line"""
        return char * width
    
    @staticmethod
    def table_separator(width=80, char="="):
        """Create a table separator"""
        return ColorCodes.WHITE + (char * width) + ColorCodes.RESET
    
    @staticmethod
    def format_price(price, prefix="$"):
        """Format price with color"""
        return f"{ColorCodes.CYAN}{prefix}{price:.8f}{ColorCodes.RESET}"
    
    @staticmethod
    def format_profit(amount, prefix="$"):
        """Format profit/loss with appropriate color"""
        if amount >= 0:
            return f"{ColorCodes.GREEN}{prefix}{amount:.2f}{ColorCodes.RESET}"
        else:
            return f"{ColorCodes.RED}{prefix}{amount:.2f}{ColorCodes.RESET}"
    
    @staticmethod
    def format_percentage(percentage):
        """Format percentage with appropriate color"""
        if percentage >= 0:
            return f"{ColorCodes.GREEN}{percentage:.4f}%{ColorCodes.RESET}"
        else:
            return f"{ColorCodes.RED}{percentage:.4f}%{ColorCodes.RESET}"


class TradingBotLogger:
    """Main logger class with both console and file output"""
    
    def __init__(self, name="TradingBot", log_file="trading_bot.log", log_level="INFO"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper()))
        self.formatter = TerminalFormatter()
        
        # Ensure logs directory exists
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # File handler (plain text)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        
        # Console handler (colored)
        console_handler = colorlog.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s - %(levelname)s - %(message)s%(reset)s',
            datefmt='%H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'white',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        console_handler.setFormatter(console_formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message):
        """Log info message"""
        self.logger.info(message)
    
    def debug(self, message):
        """Log debug message"""
        self.logger.debug(message)
    
    def warning(self, message):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message):
        """Log error message"""
        self.logger.error(message)
    
    def success(self, message):
        """Log success message in green"""
        self.logger.info(self.formatter.success(message))
    
    def print_separator(self, width=80):
        """Print separator line"""
        print(self.formatter.table_separator(width))
    
    def print_header(self, text, width=80):
        """Print header with separator"""
        self.print_separator(width)
        print(self.formatter.header(text.center(width)))
        self.print_separator(width)
    
    def print_price_comparison_table(self, chain, pair, data):
        """
        Print a formatted price comparison table
        
        Args:
            chain: Chain name (e.g., "POLYGON")
            pair: Trading pair (e.g., "USDC/WETH")
            data: List of dicts with keys: source, price, liquidity, spread
        """
        header = f"PRICE COMPARISON - {chain} | {pair}"
        self.print_header(header, 60)
        
        # Table header
        print(f"{'Source':<20} {'Price':<20} {'Liquidity':<20} {'Spread%':<10}")
        
        # Table rows
        for row in data:
            source = row.get('source', 'Unknown')
            price = row.get('price', 0)
            liquidity = row.get('liquidity', 0)
            spread = row.get('spread', None)
            
            price_str = self.formatter.format_price(price)
            liq_str = f"{liquidity:,.2f}"
            spread_str = f"{spread:.4f}" if spread is not None else ""
            
            print(f"{source:<20} {price_str:<30} {liq_str:<20} {spread_str:<10}")
        
        # Summary
        if data:
            prices = [row['price'] for row in data if 'price' in row]
            if prices:
                min_price = min(prices)
                max_price = max(prices)
                spread_pct = ((max_price - min_price) / min_price) * 100 if min_price > 0 else 0
                
                self.print_separator(60)
                summary = f"Price Range: ${min_price:.2f} - ${max_price:.2f} | Spread: {spread_pct:.4f}%"
                print(self.formatter.debug(summary))
    
    def print_execution_results(self, tx_hash, block_number, gas_used, exec_time,
                                entry_price, exit_price, gross_profit, flash_fee, net_profit, roi):
        """Print execution results"""
        self.print_header("EXECUTION RESULTS", 78)
        
        print(f"Transaction Hash: {self.formatter.info(tx_hash)}")
        print(f"Block Number: {block_number:,}")
        print(f"Gas Used: {gas_used:,}")
        print(f"Execution Time: {exec_time:.2f}s")
        print()
        print(f"Entry Price: {self.formatter.format_price(entry_price)}")
        print(f"Exit Price: {self.formatter.format_price(exit_price)}")
        print(f"Price Difference: {self.formatter.format_price(exit_price - entry_price)}")
        print()
        print(f"Gross Profit: {self.formatter.format_profit(gross_profit)}")
        print(f"Flash Loan Fee: {self.formatter.format_profit(-flash_fee)}")
        print(f"Net Profit: {self.formatter.format_profit(net_profit)}")
        print(f"ROI: {self.formatter.format_percentage(roi)}")
        
        self.print_separator(78)
    
    def print_trading_statistics(self, total_trades, winning_trades, total_profit, 
                                 total_loss, net_profit):
        """Print trading statistics"""
        self.print_header("TRADING STATISTICS", 78)
        
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        avg_profit = net_profit / total_trades if total_trades > 0 else 0
        
        print(f"Total Trades: {total_trades}")
        print(f"Winning Trades: {winning_trades}")
        print(f"Win Rate: {win_rate:.2f}%")
        print(f"Total Profit: {self.formatter.format_profit(total_profit)}")
        print(f"Total Loss: {self.formatter.format_profit(total_loss)}")
        print(f"Net Profit: {self.formatter.format_profit(net_profit)}")
        print(f"Average Profit per Trade: {self.formatter.format_profit(avg_profit)}")
        
        self.print_separator(78)
    
    def print_cycle_header(self, cycle_num, timestamp=None):
        """Print bot cycle header"""
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print("\n" + self.formatter.table_separator(84, "█"))
        header = f"CYCLE #{cycle_num} - {timestamp}"
        print(self.formatter.header(header.center(84)))
        print(self.formatter.table_separator(84, "█"))
        print()
    
    def log_opportunity(self, strategy, expected_profit, roi, rank=None):
        """Log opportunity found"""
        rank_str = f" (Rank #{rank})" if rank else ""
        msg = (f"[OPPORTUNITY FOUND - {strategy}]{rank_str}\n"
               f"  Expected Profit: {self.formatter.format_profit(expected_profit)} "
               f"({self.formatter.format_percentage(roi)})")
        self.logger.info(self.formatter.success(msg))


def setup_logger(name="TradingBot", log_file="trading_bot.log", log_level="INFO"):
    """
    Setup and return a logger instance
    
    Args:
        name: Logger name
        log_file: Path to log file
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
    
    Returns:
        TradingBotLogger instance
    """
    return TradingBotLogger(name, log_file, log_level)
