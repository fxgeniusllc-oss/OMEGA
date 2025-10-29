# Terminal Output Features

This document describes the enhanced terminal output features of the OMEGA Trading Bot.

## 🎨 Color-Coded Messages

The bot uses color-coding to make information easy to scan at a glance:

| Color | Purpose | Examples |
|-------|---------|----------|
| 🟢 **Green** | Profits, successes, positive results | Net profit, winning trades, successful executions |
| 🔴 **Red** | Losses, errors, warnings | Net losses, failed trades, error messages |
| 🔵 **Blue** | Transaction hashes, blockchain events | Transaction IDs, block numbers |
| 🟦 **Cyan** | Price data, debug info | Token prices, price differences |
| 🟡 **Yellow** | Warnings | Configuration warnings, rate limits |

## 📊 Price Comparison Tables

Display real-time price comparisons across multiple DEXs:

```
============================================================
           PRICE COMPARISON - POLYGON | USDC/WETH           
============================================================
Source               Price                Liquidity            Spread%        
Uniswap V3          $1850.50000000        500,000.00           0.0950
QuickSwap           $1850.60000000        450,000.00           
Balancer            $1851.23000000        300,000.00           
============================================================
Price Range: $1850.50 - $1851.23 | Spread: 0.0395%
```

### Features:
- Real-time price data from multiple sources
- Liquidity information
- Spread calculations
- Price range summary

## 💰 Execution Results

Detailed execution information for each trade:

```
==============================================================================
                              EXECUTION RESULTS                               
==============================================================================
Transaction Hash: 0x1a2b3c4d5e6f...
Block Number: 45,001,234
Gas Used: 287,456
Execution Time: 2.34s

Entry Price: $1850.50000000
Exit Price: $1851.23000000
Price Difference: $0.73000000

Gross Profit: $73.00
Flash Loan Fee: -$0.15
Net Profit: $72.85
ROI: 0.3925%
==============================================================================
```

### Features:
- Transaction confirmation details
- Price entry/exit points
- Profit/loss breakdown
- ROI calculation
- Gas usage tracking

## 📈 Trading Statistics

Cumulative statistics tracking:

```
==============================================================================
                              TRADING STATISTICS                              
==============================================================================
Total Trades: 5
Winning Trades: 4
Win Rate: 80.00%
Total Profit: $342.15
Total Loss: -$28.50
Net Profit: $313.65
Average Profit per Trade: $62.73
==============================================================================
```

### Features:
- Trade count and win rate
- Profit/loss summary
- Average performance metrics
- Real-time updates

## 🔄 Bot Cycle Display

Clear cycle headers with timestamps:

```
████████████████████████████████████████████████████████████████████████████████████
                           CYCLE #1 - 2024-10-29 14:23:45
████████████████████████████████████████████████████████████████████████████████████

[BOT CYCLE] Scanning for trading opportunities...
[CROSS-CHAIN ARBITRAGE] Scanning for opportunities...
[OPPORTUNITY FOUND - CROSS-CHAIN ARB]
  Expected Profit: $72.85 (0.3925%)
[EXECUTION] Found profitable opportunity (Rank #1)
```

### Features:
- Cycle numbering
- Timestamps
- Progress indicators
- Opportunity rankings

## 📋 Logged Information

### Each Cycle Logs:
✅ Strategy scanning status
✅ Price comparisons from all sources
✅ Opportunity rankings
✅ Step-by-step execution progress
✅ Entry/exit prices & slippage
✅ Transaction hashes & block numbers
✅ Gas used & execution time
✅ Profit/loss calculations
✅ Win rates & statistics

## 🚀 Usage

### Run Demo
```bash
python scripts/demo.py
```

### Run Full Bot
```bash
# Set environment variables
export AUTO_START_ARBITRAGE=true
export ACTIVE_STRATEGIES=CROSS_CHAIN_ARBITRAGE,BRIDGE_ARBITRAGE

# Run bot
python -m src.bot
```

### Configuration

Edit `.env` file to configure:

```env
# Enable/disable features
AUTO_START_ARBITRAGE=true
ACTIVE_STRATEGIES=CROSS_CHAIN_ARBITRAGE,BRIDGE_ARBITRAGE

# Logging
LOG_FILE=trading_bot.log
LOG_LEVEL=INFO

# Scan settings
SCAN_CYCLE_INTERVAL_MS=5000
```

## 📝 Logging

The bot maintains dual logging:

1. **Console (Colored)**: Real-time colored output for monitoring
2. **File (Plain)**: Complete log file at `logs/trading_bot.log` for record-keeping

Both logs contain:
- All strategy scans
- Price discoveries
- Execution results
- Error messages
- Performance statistics

## 🎯 Best Practices

1. **Monitor the Console**: Watch for green (profit) and red (loss) indicators
2. **Review Log Files**: Check `trading_bot.log` for historical data
3. **Track Statistics**: Use the statistics display to monitor overall performance
4. **Set Alerts**: Configure Telegram/email notifications for important events

## 🔧 Customization

### Custom Colors

Edit `src/logger.py` to customize colors:

```python
class ColorCodes:
    GREEN = Fore.GREEN      # Customize success color
    RED = Fore.RED          # Customize error color
    BLUE = Fore.BLUE        # Customize info color
    CYAN = Fore.CYAN        # Customize debug color
    YELLOW = Fore.YELLOW    # Customize warning color
```

### Custom Formatters

Add custom formatters in `src/logger.py`:

```python
@staticmethod
def custom_format(message):
    """Your custom formatter"""
    return f"{ColorCodes.CUSTOM}{message}{ColorCodes.RESET}"
```

## 📊 Example Output

See `scripts/demo.py` for a complete demonstration of all features. The demo runs several bot cycles showcasing:
- Price comparison tables
- Execution results
- Trading statistics
- Color-coded messages
- Bot cycle displays

## 🐛 Troubleshooting

### Colors Not Showing
- **Windows**: Ensure colorama is installed
- **Linux/Mac**: Most terminals support colors by default
- **Solution**: Run `pip install colorama`

### Log File Issues
- Ensure `logs/` directory exists
- Check file permissions
- Verify `LOG_FILE` path in `.env`

## 📚 API Reference

### TradingBotLogger

Main logger class with colored output methods:

```python
logger = setup_logger("BotName", "bot.log", "INFO")

# Basic logging
logger.info("Information message")
logger.debug("Debug message")
logger.warning("Warning message")
logger.error("Error message")
logger.success("Success message")

# Formatted tables
logger.print_price_comparison_table(chain, pair, data)
logger.print_execution_results(tx_hash, block, gas, ...)
logger.print_trading_statistics(total, winning, profit, ...)
logger.print_cycle_header(cycle_num, timestamp)

# Formatted messages
logger.log_opportunity(strategy, profit, roi, rank)
```

### TerminalFormatter

Static formatter methods:

```python
from src.logger import TerminalFormatter

# Color formatting
TerminalFormatter.success("Success message")
TerminalFormatter.error("Error message")
TerminalFormatter.info("Info message")
TerminalFormatter.debug("Debug message")
TerminalFormatter.warning("Warning message")

# Specialized formatting
TerminalFormatter.format_price(1850.50)
TerminalFormatter.format_profit(72.85)
TerminalFormatter.format_percentage(0.3925)
TerminalFormatter.separator(80, "=")
```

## 🎓 Examples

### Example 1: Basic Logging

```python
from src.logger import setup_logger

logger = setup_logger("MyBot", "mybot.log", "INFO")
logger.info("Bot started")
logger.success("Trade executed successfully")
logger.error("Failed to connect to RPC")
```

### Example 2: Price Comparison

```python
data = [
    {'source': 'Uniswap V3', 'price': 1850.50, 'liquidity': 500000, 'spread': 0.095},
    {'source': 'QuickSwap', 'price': 1850.60, 'liquidity': 450000, 'spread': None}
]
logger.print_price_comparison_table("POLYGON", "USDC/WETH", data)
```

### Example 3: Execution Results

```python
logger.print_execution_results(
    tx_hash="0x1a2b3c...",
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
```

## 🔐 Security Notes

- Log files may contain sensitive information
- Avoid logging private keys or API secrets
- Secure log file access with appropriate permissions
- Consider log rotation for production deployments

## 📄 License

See LICENSE file for details.
