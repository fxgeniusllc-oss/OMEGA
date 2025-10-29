"""
Unified Trading Bot with Enhanced Terminal Output
Displays color-coded price comparisons, execution results, and statistics
"""
import asyncio
import time
from datetime import datetime
from typing import List, Dict
import random

from src.logger import setup_logger
from src.config import Config
from src.strategies.arbitrage import CrossChainArbitrageStrategy, BridgeArbitrageStrategy


class TradingStatistics:
    """Track trading statistics"""
    
    def __init__(self):
        self.total_trades = 0
        self.winning_trades = 0
        self.total_profit = 0.0
        self.total_loss = 0.0
        self.net_profit = 0.0
        self.trade_history = []
    
    def add_trade(self, result: Dict):
        """Add a trade to statistics"""
        self.total_trades += 1
        net_profit = result.get('net_profit', 0)
        
        if net_profit > 0:
            self.winning_trades += 1
            self.total_profit += net_profit
        else:
            self.total_loss += abs(net_profit)
        
        self.net_profit = self.total_profit - self.total_loss
        self.trade_history.append(result)
    
    def get_stats(self) -> Dict:
        """Get statistics summary"""
        return {
            'total_trades': self.total_trades,
            'winning_trades': self.winning_trades,
            'total_profit': self.total_profit,
            'total_loss': -self.total_loss,
            'net_profit': self.net_profit
        }


class UnifiedTradingBot:
    """Main trading bot with enhanced terminal output"""
    
    def __init__(self):
        # Initialize configuration
        self.config = Config()
        
        # Setup logger
        self.logger = setup_logger(
            name="UnifiedTradingBot",
            log_file=self.config.LOG_FILE,
            log_level=self.config.LOG_LEVEL
        )
        
        # Initialize statistics
        self.stats = TradingStatistics()
        
        # Initialize strategies
        self.strategies = []
        self._initialize_strategies()
        
        # Bot state
        self.cycle_count = 0
        self.running = False
    
    def _initialize_strategies(self):
        """Initialize active strategies"""
        active_strategies = self.config.get_active_strategies()
        
        if 'CROSS_CHAIN_ARBITRAGE' in active_strategies:
            strategy = CrossChainArbitrageStrategy(
                self.logger,
                min_profit_usd=self.config.MIN_PROFIT_USD
            )
            self.strategies.append(strategy)
            self.logger.info(f"Initialized strategy: {strategy.name}")
        
        if 'BRIDGE_ARBITRAGE' in active_strategies:
            strategy = BridgeArbitrageStrategy(
                self.logger,
                min_profit_usd=self.config.MIN_PROFIT_USD
            )
            self.strategies.append(strategy)
            self.logger.info(f"Initialized strategy: {strategy.name}")
    
    def display_price_comparison(self, chain: str = "POLYGON", pair: str = "USDC/WETH"):
        """Display price comparison table"""
        # Generate mock price data
        base_price = 1850.50
        data = [
            {
                'source': 'Uniswap V3',
                'price': base_price + random.uniform(-2, 2),
                'liquidity': 500000.00,
                'spread': 0.0950
            },
            {
                'source': 'QuickSwap',
                'price': base_price + random.uniform(-1, 3),
                'liquidity': 450000.00,
                'spread': None
            },
            {
                'source': 'Balancer',
                'price': base_price + random.uniform(0, 4),
                'liquidity': 300000.00,
                'spread': None
            }
        ]
        
        self.logger.print_price_comparison_table(chain, pair, data)
    
    async def scan_all_strategies(self) -> List[Dict]:
        """Scan all strategies for opportunities"""
        all_opportunities = []
        
        # Scan strategies concurrently
        tasks = [strategy.scan_for_opportunities() for strategy in self.strategies]
        results = await asyncio.gather(*tasks)
        
        # Combine all opportunities
        for opportunities in results:
            all_opportunities.extend(opportunities)
        
        # Rank opportunities by expected profit
        all_opportunities.sort(key=lambda x: x.get('expected_profit', 0), reverse=True)
        
        # Add rank
        for i, opp in enumerate(all_opportunities, 1):
            opp['rank'] = i
        
        return all_opportunities
    
    async def execute_opportunity(self, opportunity: Dict) -> Dict:
        """Execute a trading opportunity"""
        # Find the strategy that found this opportunity
        strategy_name = opportunity.get('strategy')
        strategy = next((s for s in self.strategies if s.name == strategy_name), None)
        
        if not strategy:
            self.logger.error(f"Strategy {strategy_name} not found")
            return {'success': False}
        
        # Execute
        rank = opportunity.get('rank', 'N/A')
        self.logger.info(f"[EXECUTION] Found profitable opportunity (Rank #{rank})")
        
        result = await strategy.execute_opportunity(opportunity)
        
        # Display execution results
        if result.get('success'):
            self.logger.print_execution_results(
                tx_hash=result['tx_hash'],
                block_number=result['block_number'],
                gas_used=result['gas_used'],
                exec_time=result['execution_time'],
                entry_price=result['entry_price'],
                exit_price=result['exit_price'],
                gross_profit=result['gross_profit'],
                flash_fee=result['flash_fee'],
                net_profit=result['net_profit'],
                roi=result['roi']
            )
            
            # Update statistics
            self.stats.add_trade(result)
        
        return result
    
    def display_statistics(self):
        """Display trading statistics"""
        stats = self.stats.get_stats()
        
        self.logger.print_trading_statistics(
            total_trades=stats['total_trades'],
            winning_trades=stats['winning_trades'],
            total_profit=stats['total_profit'],
            total_loss=stats['total_loss'],
            net_profit=stats['net_profit']
        )
    
    async def run_cycle(self):
        """Run a single bot cycle"""
        self.cycle_count += 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Display cycle header
        self.logger.print_cycle_header(self.cycle_count, timestamp)
        
        # Log cycle start
        self.logger.info("[BOT CYCLE] Scanning for trading opportunities...")
        
        # Optionally display price comparison
        if self.cycle_count % 3 == 1:  # Every 3rd cycle
            self.display_price_comparison()
        
        # Scan for opportunities
        opportunities = await self.scan_all_strategies()
        
        # Execute best opportunity if found
        if opportunities:
            best_opportunity = opportunities[0]
            await self.execute_opportunity(best_opportunity)
            
            # Display statistics every few cycles
            if self.cycle_count % 2 == 0:
                self.display_statistics()
        else:
            self.logger.info("No profitable opportunities found in this cycle")
    
    async def start(self):
        """Start the trading bot"""
        self.running = True
        
        # Display startup message
        self.logger.print_header("UNIFIED TRADING BOT STARTED", 84)
        self.logger.info(f"Mode: {self.config.MODE}")
        self.logger.info(f"Auto Start: {self.config.AUTO_START_ARBITRAGE}")
        self.logger.info(f"Live Execution: {self.config.LIVE_EXECUTION}")
        self.logger.info(f"Active Strategies: {', '.join(self.config.get_active_strategies())}")
        self.logger.info(f"Scan Interval: {self.config.SCAN_CYCLE_INTERVAL_MS}ms")
        print()
        
        # Run cycles
        try:
            while self.running:
                await self.run_cycle()
                
                # Wait for next cycle
                await asyncio.sleep(self.config.SCAN_CYCLE_INTERVAL_MS / 1000)
        
        except KeyboardInterrupt:
            self.logger.info("\nShutdown requested by user")
            self.stop()
        except Exception as e:
            self.logger.error(f"Bot error: {e}")
            raise
    
    def stop(self):
        """Stop the trading bot"""
        self.running = False
        self.logger.print_header("TRADING BOT STOPPED", 84)
        
        # Display final statistics
        if self.stats.total_trades > 0:
            self.display_statistics()
        
        self.logger.info("Bot shutdown complete")


async def main():
    """Main entry point"""
    bot = UnifiedTradingBot()
    
    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        print(f"Configuration error: {e}")
        return
    
    # Start bot
    await bot.start()


if __name__ == "__main__":
    # Run the bot
    asyncio.run(main())
