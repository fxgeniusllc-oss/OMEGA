"""Unified trading bot orchestrating all strategies."""
import asyncio
from typing import List, Dict, Optional
from src.config import Config
from src.logger import Logger
from src.blockchain import BlockchainInterface
from src.oracle import PriceOracle
from src.position_manager import PositionManager
from src.flash_loan_manager import FlashLoanManager
from src.strategies import (
    MempoolWatcher,
    CrossChainArbitrageur,
    BridgeArbitrageur,
    PumpPredictionAI,
    MarketMaker,
    StatisticalArbitrageur,
    GammaScalper,
    FundingRateHarvester,
    VolatilityArbitrageur,
)
from src.utils import rank_opportunities, calculate_profit_after_fees


class UnifiedTradingBot:
    """
    Unified trading bot that orchestrates all strategies.
    
    Features:
    - Single orchestration class for all strategies
    - Configuration-driven strategy enablement
    - Multi-chain support (Polygon, Ethereum, Arbitrum, Optimism)
    - Position management with Kelly Criterion sizing
    - Flash loan integration (Balancer/Aave)
    - Opportunity ranking by profit * confidence
    - Comprehensive logging and error handling
    """
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize unified trading bot."""
        self.config = config or Config
        self.logger = Logger.setup(
            log_file=self.config.LOG_FILE,
            log_level=self.config.LOG_LEVEL
        )
        
        self.logger.info("=" * 80)
        self.logger.info("Initializing Unified Trading Bot")
        self.logger.info(f"Mode: {self.config.MODE}")
        self.logger.info(f"Bot Address: {self.config.BOT_ADDRESS}")
        self.logger.info("=" * 80)
        
        # Initialize core components
        self.blockchain = BlockchainInterface(self.config)
        self.oracle = PriceOracle()
        self.position_manager = PositionManager(self.config, self.logger)
        self.flash_loan_manager = FlashLoanManager(
            self.config, self.blockchain, self.logger
        )
        
        # Initialize strategies
        self.strategies = self._initialize_strategies()
        
        # Create a mapping from class names to strategy instances
        self.strategy_by_name = {
            strategy.name: strategy
            for strategy in self.strategies.values()
        }
        
        # Bot state
        self.running = False
        self.total_profit = 0.0
        self.total_trades = 0
        
    def _initialize_strategies(self) -> Dict:
        """Initialize all available strategies."""
        all_strategies = {
            'MEMPOOL_WATCHING': MempoolWatcher(
                self.config, self.blockchain, self.oracle, self.logger
            ),
            'CROSS_CHAIN_ARBITRAGE': CrossChainArbitrageur(
                self.config, self.blockchain, self.oracle, self.logger
            ),
            'BRIDGE_ARBITRAGE': BridgeArbitrageur(
                self.config, self.blockchain, self.oracle, self.logger
            ),
            'PUMP_PREDICTION': PumpPredictionAI(
                self.config, self.blockchain, self.oracle, self.logger
            ),
            'MARKET_MAKING': MarketMaker(
                self.config, self.blockchain, self.oracle, self.logger
            ),
            'STATISTICAL_ARBITRAGE': StatisticalArbitrageur(
                self.config, self.blockchain, self.oracle, self.logger
            ),
            'GAMMA_SCALPING': GammaScalper(
                self.config, self.blockchain, self.oracle, self.logger
            ),
            'FUNDING_RATE': FundingRateHarvester(
                self.config, self.blockchain, self.oracle, self.logger
            ),
            'VOLATILITY_ARBITRAGE': VolatilityArbitrageur(
                self.config, self.blockchain, self.oracle, self.logger
            ),
        }
        
        # Enable only active strategies
        active_strategies = {}
        for strategy_name in self.config.ACTIVE_STRATEGIES:
            strategy_name = strategy_name.strip()
            if strategy_name in all_strategies:
                active_strategies[strategy_name] = all_strategies[strategy_name]
                self.logger.info(f"✓ Strategy enabled: {strategy_name}")
            else:
                self.logger.warning(f"✗ Unknown strategy: {strategy_name}")
        
        return active_strategies
    
    async def start(self):
        """Start the trading bot."""
        self.running = True
        self.logger.info("Trading bot started")
        
        # Update initial capital
        await self._update_capital()
        
        # Log blockchain connections
        self._log_connections()
        
        # Main trading loop
        while self.running:
            try:
                await self._trading_cycle()
                await asyncio.sleep(5)  # Wait between cycles
            except KeyboardInterrupt:
                self.logger.info("Received shutdown signal")
                break
            except Exception as e:
                self.logger.error(f"Trading cycle error: {e}")
                await asyncio.sleep(10)
        
        self.logger.info("Trading bot stopped")
    
    async def _trading_cycle(self):
        """Execute one trading cycle."""
        self.logger.info("-" * 80)
        self.logger.info("Starting trading cycle")
        
        # Scan all strategies for opportunities
        all_opportunities = await self._scan_all_strategies()
        
        if not all_opportunities:
            self.logger.info("No opportunities found this cycle")
            return
        
        # Rank opportunities by profit * confidence
        ranked_opportunities = rank_opportunities(all_opportunities)
        
        self.logger.info(f"Found {len(ranked_opportunities)} opportunities")
        
        # Execute top opportunities
        executed_count = 0
        for opp in ranked_opportunities[:5]:  # Execute top 5
            success = await self._execute_opportunity(opp)
            if success:
                executed_count += 1
        
        self.logger.info(f"Executed {executed_count} trades this cycle")
        self.logger.info(f"Total profit: ${self.total_profit:.2f}")
    
    async def _scan_all_strategies(self) -> List[Dict]:
        """Scan all enabled strategies for opportunities."""
        all_opportunities = []
        
        # Run all strategies concurrently
        tasks = [
            strategy.run()
            for strategy in self.strategies.values()
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, Exception):
                self.logger.error(f"Strategy scan error: {result}")
            elif isinstance(result, list):
                all_opportunities.extend(result)
        
        return all_opportunities
    
    async def _execute_opportunity(self, opportunity: Dict) -> bool:
        """
        Execute a trading opportunity.
        
        Args:
            opportunity: Opportunity details
        
        Returns:
            True if execution successful
        """
        try:
            strategy_name = opportunity.get('strategy')
            estimated_profit = opportunity.get('estimated_profit', 0)
            gas_cost = opportunity.get('gas_cost', 0)
            confidence = opportunity.get('confidence', 0)
            
            # Calculate net profit
            net_profit = calculate_profit_after_fees(estimated_profit, gas_cost)
            
            # Check if flash loan is needed
            amount = opportunity.get('amount', 0)
            use_flash_loan = amount > self.position_manager.total_capital
            
            if use_flash_loan:
                flash_loan_fee = self.flash_loan_manager.calculate_flash_loan_fee(amount)
                net_profit -= flash_loan_fee
                
                if net_profit <= 0:
                    self.logger.warning(
                        f"Skipping opportunity: Flash loan fee makes it unprofitable"
                    )
                    return False
            
            # Calculate position size
            position_size = self.position_manager.calculate_position_size(
                strategy_name=strategy_name,
                win_probability=confidence,
                expected_profit=net_profit,
                expected_loss=gas_cost,
            )
            
            if position_size <= 0:
                self.logger.warning("Position size is zero, skipping")
                return False
            
            # Execute through strategy
            strategy = self.strategy_by_name.get(strategy_name)
            if not strategy:
                self.logger.error(f"Strategy not found: {strategy_name}")
                return False
            
            self.logger.info(
                f"Executing opportunity: {strategy_name} | "
                f"Profit ${net_profit:.2f} | Confidence {confidence:.2%}"
            )
            
            success = await strategy.execute_opportunity(opportunity)
            
            if success:
                self.total_profit += net_profit
                self.total_trades += 1
                self.logger.info(f"✓ Trade executed successfully | Profit ${net_profit:.2f}")
            else:
                self.logger.warning("✗ Trade execution failed")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Execution error: {e}")
            return False
    
    async def _update_capital(self):
        """Update available capital from blockchain."""
        try:
            # In SIM mode, use mock capital
            if self.config.MODE == "SIM":
                self.position_manager.update_capital(100000.0)
                return
            
            # Get balance from primary chain (Polygon)
            balance = await self.blockchain.get_balance(
                "POLYGON",
                self.config.BOT_ADDRESS
            )
            
            # Convert to USD (mock)
            matic_price = await self.oracle.get_price("MATIC", "USD")
            if matic_price and balance > 0:
                capital_usd = balance * matic_price
                self.position_manager.update_capital(capital_usd)
            else:
                # Fallback to mock capital for simulation
                self.position_manager.update_capital(10000.0)
                
        except Exception as e:
            self.logger.error(f"Error updating capital: {e}")
            # Use mock capital
            self.position_manager.update_capital(10000.0)
    
    def _log_connections(self):
        """Log blockchain connection status."""
        self.logger.info("Blockchain connections:")
        for chain_name in ["POLYGON", "ETHEREUM", "ARBITRUM", "OPTIMISM"]:
            connected = self.blockchain.is_connected(chain_name)
            status = "✓ Connected" if connected else "✗ Not connected"
            self.logger.info(f"  {chain_name}: {status}")
    
    def stop(self):
        """Stop the trading bot."""
        self.running = False
        self.logger.info("Stopping trading bot...")
    
    def get_status(self) -> Dict:
        """Get bot status and statistics."""
        return {
            'running': self.running,
            'mode': self.config.MODE,
            'total_profit': self.total_profit,
            'total_trades': self.total_trades,
            'active_strategies': list(self.strategies.keys()),
            'position_metrics': self.position_manager.get_risk_metrics(),
            'strategy_stats': {
                name: strategy.get_stats()
                for name, strategy in self.strategies.items()
            }
        }


async def main():
    """Main entry point."""
    bot = UnifiedTradingBot()
    
    try:
        await bot.start()
    except KeyboardInterrupt:
        bot.stop()
    finally:
        # Print final statistics
        status = bot.get_status()
        bot.logger.info("=" * 80)
        bot.logger.info("Final Statistics")
        bot.logger.info(f"Total Trades: {status['total_trades']}")
        bot.logger.info(f"Total Profit: ${status['total_profit']:.2f}")
        bot.logger.info("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
