"""Enhanced logging setup for the trading bot."""
import logging
import sys
from pathlib import Path
from typing import Optional
import colorlog


class Logger:
    """Logger configuration and management."""
    
    _logger: Optional[logging.Logger] = None
    
    @classmethod
    def setup(cls, log_file: str = "trading_bot.log", log_level: str = "INFO") -> logging.Logger:
        """Setup and configure logger."""
        if cls._logger:
            return cls._logger
        
        # Create logs directory if it doesn't exist
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create logger
        cls._logger = logging.getLogger("TradingBot")
        cls._logger.setLevel(getattr(logging, log_level.upper()))
        
        # Console handler with colors
        console_handler = colorlog.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s [%(levelname)s]%(reset)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        console_handler.setFormatter(console_formatter)
        
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        
        # Add handlers
        cls._logger.addHandler(console_handler)
        cls._logger.addHandler(file_handler)
        
        return cls._logger
    
    @classmethod
    def get_logger(cls) -> logging.Logger:
        """Get the configured logger."""
        if not cls._logger:
            cls.setup()
        return cls._logger
