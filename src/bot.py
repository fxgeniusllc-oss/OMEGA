"""
Unified Trading Bot with Environment Configuration
"""
import asyncio
import sys
from typing import List, Dict
from datetime import datetime

from .config import config
from .logger import get_logger
from .oracle import PriceOracle
from .blockchain import BlockchainInterface
from .strategies import CrossChainArbitrage, BridgeArbitrage
from .utils.helpers import format_usd

class UnifiedTradingBot:
    """Main trading bot with full environment configuration support"""
    
    def __init__(self):
        """Initialize the trading bot"""
        # Initialize logger
        self.logger = get_logger(
            name="TradingBot",
            log_file=config.log_file,
            level=config.log_level
        )
        
        # Validate configuration
        if not config.validate():
            self.logger.error("❌ Configuration validation failed. Please check your .env file.")
            sys.exit(1)
        
        # Initialize components
        self.oracle = PriceOracle(config.coingecko_api_key)
        self.blockchain = BlockchainInterface(self.logger)
        
        # Initialize strategies
        self.strategies = []
        self._initialize_strategies()
        
        # Bot state
        self.running = False
        self.total_opportunities = 0
        self.total_trades = 0
        self.total_profit_usd = 0.0
    
    def _initialize_strategies(self):
        """Initialize trading strategies based on config"""
        strategy_map = {
            'CROSS_CHAIN_ARBITRAGE': CrossChainArbitrage,
            'BRIDGE_ARBITRAGE': BridgeArbitrage,
        }
        
        for strategy_name in config.active_strategies:
            if strategy_name in strategy_map:
                strategy_class = strategy_map[strategy_name]
                strategy = strategy_class(
                    config=config,
                    logger=self.logger,
                    blockchain=self.blockchain,
                    oracle=self.oracle
                )
                self.strategies.append(strategy)
                self.logger.info(f"✓ Initialized strategy: {strategy.name}")
            else:
                self.logger.warning(f"⚠ Unknown strategy: {strategy_name}")
    
    def display_startup_banner(self):
        """Display comprehensive startup banner"""
        self.logger.log_startup_banner(config)
        
        # Display RPC configuration
        self.logger.log_rpc_config(config)
        
        # Display DEX routers
        self.logger.log_dex_routers(config)
        
        # Display risk settings
        self.logger.log_risk_settings(config)
        
        # Display flash loan configuration
        self.logger.info(f"💰 Flash Loan Provider: {config.flashloan_provider}")
        
        # Display token configuration
        self.logger.info("🪙 Configured Tokens:")
        for token, address in config.token_addresses.items():
            if address:
                self.logger.info(f"  ✓ {token}: {address[:10]}...{address[-8:]}")
        
        # Display connection status
        self.logger.info("🌐 Chain Connection Status:")
        status = self.blockchain.get_connection_status()
        for chain, connected in status.items():
            status_icon = "✓" if connected else "✗"
            status_text = "Connected" if connected else "Disconnected"
            self.logger.info(f"  {status_icon} {chain}: {status_text}")
        
        # Display wallet balances
        self._display_wallet_balances()
        
        self.logger.log_separator()
    
    def _display_wallet_balances(self):
        """Display wallet balances for bot address"""
        if not config.bot_address:
            return
        
        self.logger.info(f"💼 Bot Wallet Balances:")
        
        for chain in config.enabled_chains:
            try:
                balance = self.blockchain.get_balance(chain, config.bot_address)
                if balance is not None:
                    # Convert to token amount (assuming 18 decimals for native tokens)
                    token_balance = balance / (10 ** 18)
                    
                    # Get native token symbol
                    native_tokens = {
                        'POLYGON': 'MATIC',
                        'ETHEREUM': 'ETH',
                        'ARBITRUM': 'ETH',
                        'OPTIMISM': 'ETH',
                        'BASE': 'ETH',
                        'BSC': 'BNB'
                    }
                    token_symbol = native_tokens.get(chain, 'TOKEN')
                    
                    # Convert to USD
                    usd_value = self.oracle.token_amount_to_usd(balance, token_symbol.replace('MATIC', 'WMATIC'))
                    
                    self.logger.info(f"  {chain}: {token_balance:.4f} {token_symbol} (${usd_value:.2f})")
            except Exception as e:
                self.logger.debug(f"  {chain}: Could not fetch balance - {e}")
    
    async def scan_cycle(self):
        """Single scan cycle across all strategies"""
        all_opportunities = []
        
        # Scan with all strategies
        for strategy in self.strategies:
            if strategy.enabled:
                try:
                    opportunities = await strategy.scan()
                    all_opportunities.extend(opportunities)
                except Exception as e:
                    self.logger.error(f"Error in {strategy.name} scan: {e}")
        
        # Update total opportunities
        self.total_opportunities += len(all_opportunities)
        
        # Execute opportunities if auto-trading is enabled
        if config.auto_trading_enabled and all_opportunities:
            await self._execute_opportunities(all_opportunities)
        
        return all_opportunities
    
    async def _execute_opportunities(self, opportunities: List[Dict]):
        """Execute found opportunities"""
        # Sort by profit (highest first)
        opportunities.sort(key=lambda x: x.get('profit_usd', 0), reverse=True)
        
        for opp in opportunities:
            # Check if opportunity meets confidence threshold
            if opp.get('confidence', 0) < config.confidence_threshold:
                continue
            
            # Find the strategy that found this opportunity
            strategy = next(
                (s for s in self.strategies if s.name == opp['strategy']),
                None
            )
            
            if strategy:
                try:
                    success = await strategy.execute(opp)
                    if success:
                        self.total_trades += 1
                        self.total_profit_usd += opp.get('profit_usd', 0)
                except Exception as e:
                    self.logger.error(f"Error executing trade: {e}")
    
    async def run(self):
        """Main bot loop"""
        self.running = True
        self.logger.info("🚀 Bot started - Beginning scan cycles...")
        self.logger.log_separator()
        
        scan_count = 0
        start_time = datetime.now()
        
        try:
            while self.running:
                scan_count += 1
                
                # Log scan cycle
                if scan_count % 10 == 0:  # Log every 10 cycles
                    uptime = (datetime.now() - start_time).total_seconds()
                    self.logger.info(f"📊 Stats: Scan #{scan_count} | Uptime: {uptime:.0f}s | Opportunities: {self.total_opportunities} | Trades: {self.total_trades} | Profit: ${self.total_profit_usd:.2f}")
                
                # Run scan cycle
                await self.scan_cycle()
                
                # Wait before next cycle
                await asyncio.sleep(config.scan_cycle_interval_ms / 1000.0)
                
        except KeyboardInterrupt:
            self.logger.info("\n⚠️  Keyboard interrupt received. Shutting down...")
        except Exception as e:
            self.logger.error(f"❌ Unexpected error: {e}")
        finally:
            await self.shutdown()
    
    async def shutdown(self):
        """Shutdown bot gracefully"""
        self.running = False
        self.logger.log_separator()
        self.logger.info("👋 Bot shutdown initiated")
        
        # Display final statistics
        self.logger.info("📊 Final Statistics:")
        self.logger.info(f"  Total Opportunities Found: {self.total_opportunities}")
        self.logger.info(f"  Total Trades Executed: {self.total_trades}")
        self.logger.info(f"  Total Profit (USD): {format_usd(self.total_profit_usd)}")
        
        # Display strategy statistics
        self.logger.info("📈 Strategy Performance:")
        for strategy in self.strategies:
            stats = strategy.get_stats()
            self.logger.info(f"  {stats['name']}:")
            self.logger.info(f"    Opportunities: {stats['opportunities_found']}")
            self.logger.info(f"    Trades: {stats['trades_executed']}")
        
        self.logger.log_separator()
        self.logger.info("✅ Bot shutdown complete")

async def main():
    """Main entry point"""
    print("\n" + "="*80)
    print("DeFi Trading Bot - Environment Configuration")
    print("="*80 + "\n")
    
    # Create and run bot
    bot = UnifiedTradingBot()
    bot.display_startup_banner()
    
    # Start the bot
    if config.auto_start_arbitrage:
        await bot.run()
    else:
        bot.logger.info("ℹ️  AUTO_START_ARBITRAGE is disabled. Bot initialized but not started.")
        bot.logger.info("   Set AUTO_START_ARBITRAGE=true in .env to start automatically.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n✅ Bot terminated by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)
