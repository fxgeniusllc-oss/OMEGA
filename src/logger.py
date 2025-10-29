"""
Enhanced logging setup with colorized output
"""
import logging
import sys
from pathlib import Path
from datetime import datetime
from colorlog import ColoredFormatter

class BotLogger:
    """Enhanced logger for trading bot with colorized output"""
    
    def __init__(self, name: str = "TradingBot", log_file: str = "trading_bot.log", level: str = "INFO"):
        self.name = name
        self.log_file = log_file
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        
        # Remove existing handlers
        self.logger.handlers = []
        
        # Create logs directory if it doesn't exist
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Console handler with colors
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        
        # Colored formatter for console
        console_format = (
            '%(log_color)s%(asctime)s%(reset)s | '
            '%(log_color)s%(levelname)-8s%(reset)s | '
            '%(cyan)s%(name)s%(reset)s | '
            '%(message)s'
        )
        
        console_formatter = ColoredFormatter(
            console_format,
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        console_handler.setFormatter(console_formatter)
        
        # File handler (no colors)
        file_handler = logging.FileHandler(log_dir / log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        file_format = (
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
        )
        file_formatter = logging.Formatter(file_format, datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(file_formatter)
        
        # Add handlers
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def info(self, message: str):
        """Log info message"""
        self.logger.info(message)
    
    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)
    
    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log error message"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Log critical message"""
        self.logger.critical(message)
    
    def log_separator(self, char: str = "═", length: int = 80):
        """Log a separator line"""
        self.logger.info(char * length)
    
    def log_startup_banner(self, config):
        """Log comprehensive startup banner"""
        self.log_separator()
        self.info("BOT STARTUP - USING YOUR ENVIRONMENT CONFIGURATION")
        self.log_separator()
        self.info(f"Mode: {config.mode}")
        self.info(f"Chains: {', '.join(config.enabled_chains)}")
        
        # Format DEX names
        dex_names = []
        for dex in config.active_dexs:
            if dex == "UNISWAP_V3":
                dex_names.append("UNISWAP_V3")
            else:
                dex_names.append(dex)
        
        self.info(f"DEXs Scanning: {', '.join(dex_names)}")
        self.info(f"Strategies: {', '.join(config.active_strategies)}")
        self.info(f"Bot Address: {config.bot_address}")
        self.info(f"Executor Address: {config.executor_address}")
        self.info(f"Currency: USD (End-to-End Conversion)")
        self.log_separator()
    
    def log_rpc_config(self, config):
        """Log RPC configuration with fallbacks"""
        self.info("🌐 RPC Configuration (with fallbacks):")
        for chain in config.enabled_chains:
            rpcs = config.get_all_rpc_urls(chain)
            if rpcs:
                self.info(f"  {chain}:")
                for i, rpc in enumerate(rpcs, 1):
                    # Mask the API key in the URL
                    masked_rpc = self._mask_api_key(rpc)
                    self.info(f"    {i}. {masked_rpc}")
    
    def log_dex_routers(self, config):
        """Log configured DEX routers"""
        self.info("🔧 DEX Routers:")
        for dex in config.active_dexs:
            router = config.dex_routers.get(dex, '')
            if router:
                self.info(f"  ✓ {dex}: {router[:10]}...{router[-8:]}")
    
    def log_risk_settings(self, config):
        """Log risk management settings"""
        self.info("⚠️  Risk Management:")
        self.info(f"  Min Profit: ${config.min_profit_usd}")
        self.info(f"  Min Liquidity: ${config.min_liquidity_usd:,.0f}")
        self.info(f"  Max Trade Size: ${config.max_trade_size_usd:,.0f}")
        self.info(f"  Slippage: {config.slippage_bps / 100}%")
        self.info(f"  Gas Multiplier: {config.gas_price_multiplier}x")
    
    def log_trade(self, trade_data: dict):
        """Log trade execution"""
        self.info(f"💰 Trade Executed:")
        self.info(f"  Strategy: {trade_data.get('strategy', 'N/A')}")
        self.info(f"  DEX: {trade_data.get('dex', 'N/A')}")
        self.info(f"  Profit: ${trade_data.get('profit_usd', 0):.2f}")
        self.info(f"  Token: {trade_data.get('token', 'N/A')}")
        self.info(f"  Amount: {trade_data.get('amount', 0)}")
    
    def log_opportunity(self, opp_data: dict):
        """Log arbitrage opportunity"""
        self.info(f"🎯 Opportunity Found:")
        self.info(f"  Chain: {opp_data.get('chain', 'N/A')}")
        self.info(f"  DEX Pair: {opp_data.get('dex_pair', 'N/A')}")
        self.info(f"  Expected Profit: ${opp_data.get('profit_usd', 0):.2f}")
        self.info(f"  Confidence: {opp_data.get('confidence', 0):.2%}")
    
    def _mask_api_key(self, url: str) -> str:
        """Mask API key in URL for security"""
        if not url:
            return "Not configured"
        
        # Find the last part after the last slash
        parts = url.split('/')
        if len(parts) > 1:
            # Mask the last part (usually the API key)
            parts[-1] = parts[-1][:6] + "..." + parts[-1][-4:] if len(parts[-1]) > 10 else "***"
            return '/'.join(parts)
        return url

def get_logger(name: str = "TradingBot", log_file: str = "trading_bot.log", level: str = "INFO") -> BotLogger:
    """Get or create a logger instance"""
    return BotLogger(name, log_file, level)
