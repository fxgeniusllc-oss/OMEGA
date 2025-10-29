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
"""Main DeFi Trading Bot with USD conversion and enhanced price sources."""

import asyncio
import logging
from decimal import Decimal
from typing import Dict, List, Optional

from src.config import Config
from src.logger import setup_logger, log_price_comparison_table, log_execution_results
from src.oracle import PriceOracle
from src.utils.constants import DEX_SOURCES, BRIDGE_SOURCES, CEX_SOURCES
from src.utils.helpers import format_usd, parse_fee_percentage


class UnifiedTradingBot:
    """
    Unified Trading Bot with end-to-end USD conversion.
    
    All metrics are in USD:
    - Prices (displayed as $X.XX USD)
    - Liquidity (shown in USD)
    - Profits/losses (in USD)
    - Gas fees (converted to USD)
    - Position sizes (in USD)
    - All comparisons normalized to USD
    """
    
    def __init__(self):
        """Initialize the UnifiedTradingBot."""
        self.logger = setup_logger(
            name="TradingBot",
            log_file=Config.LOG_FILE,
            log_level=Config.LOG_LEVEL
        )
        self.oracle = PriceOracle()
        self.enabled_chains = Config.get_enabled_chains()
        
        self.logger.info("=" * 80)
        self.logger.info("🚀 UNIFIED TRADING BOT - USD CONVERSION ENABLED")
        self.logger.info("=" * 80)
        self.logger.info(f"Mode: {Config.MODE}")
        self.logger.info(f"Auto-start arbitrage: {Config.AUTO_START_ARBITRAGE}")
        self.logger.info(f"Enabled chains: {', '.join(self.enabled_chains)}")
        self.logger.info(f"Min profit (USD): {format_usd(Config.MIN_PROFIT_USD)}")
        self.logger.info(f"Min liquidity (USD): {format_usd(Config.MIN_LIQUIDITY_USD)}")
        self.logger.info("=" * 80)
        
    async def start(self):
        """Start the trading bot."""
        self.logger.info("\n🔧 Initializing price sources...")
        await self._initialize_sources()
        
        if Config.AUTO_START_ARBITRAGE:
            self.logger.info("\n🎯 Auto-starting arbitrage monitoring...")
            await self.run_arbitrage_scan()
        else:
            self.logger.info("\n⏸️  Auto-start disabled. Waiting for manual trigger...")
    
    async def _initialize_sources(self):
        """Initialize and log all price sources."""
        total_dex = sum(len(sources) for sources in DEX_SOURCES.values())
        total_bridge = len(BRIDGE_SOURCES)
        total_cex = len(CEX_SOURCES)
        
        self.logger.info(f"📊 DEX Sources: {total_dex} across {len(DEX_SOURCES)} chains")
        for chain, dexs in DEX_SOURCES.items():
            self.logger.info(f"  • {chain.upper()}: {', '.join(dexs.keys())}")
        
        self.logger.info(f"\n🌉 Bridge Sources: {total_bridge}")
        self.logger.info(f"  • {', '.join(BRIDGE_SOURCES.keys())}")
        
        self.logger.info(f"\n💱 CEX Sources: {total_cex}")
        self.logger.info(f"  • {', '.join(CEX_SOURCES.keys())}")
        
        self.logger.info(f"\n✅ Total Price Sources: {total_dex + total_bridge + total_cex}")
    
    async def run_arbitrage_scan(self):
        """Run arbitrage opportunity scan with USD conversion."""
        self.logger.info("\n" + "=" * 80)
        self.logger.info("🔍 SCANNING FOR ARBITRAGE OPPORTUNITIES (USD-BASED)")
        self.logger.info("=" * 80)
        
        # Scan for opportunities on each enabled chain
        for chain in self.enabled_chains:
            await self._scan_chain(chain)
        
        # Demonstrate cross-chain arbitrage
        await self._demonstrate_cross_chain_arbitrage()
    
    async def _scan_chain(self, chain: str):
        """
        Scan a specific chain for arbitrage opportunities.
        
        Args:
            chain: Chain name to scan
        """
        self.logger.info(f"\n🔎 Scanning {chain.upper()}...")
        
        # Example pair: WETH/USDC
        token_a = "WETH"
        token_b = "USDC"
        
        # Get price comparisons from all sources
        comparisons = await self.oracle.get_price_comparison(token_a, token_b, chain)
        
        if not comparisons:
            self.logger.warning(f"No price data available for {token_a}/{token_b} on {chain}")
            return
        
        # Log the comparison table
        log_price_comparison_table(comparisons, token_a, token_b, chain)
        
        # Find best arbitrage opportunity
        opportunity = self._find_best_opportunity(comparisons)
        
        if opportunity:
            await self._evaluate_opportunity(opportunity, token_a, chain)
    
    def _find_best_opportunity(self, comparisons: List[Dict]) -> Optional[Dict]:
        """
        Find the best arbitrage opportunity from price comparisons.
        
        Args:
            comparisons: List of price comparisons
            
        Returns:
            Best opportunity or None
        """
        if len(comparisons) < 2:
            return None
        
        # Sort by price
        sorted_comps = sorted(comparisons, key=lambda x: x["price_usd"])
        
        # Buy from cheapest, sell to most expensive
        buy_source = sorted_comps[0]
        sell_source = sorted_comps[-1]
        
        # Calculate potential profit
        price_diff = sell_source["price_usd"] - buy_source["price_usd"]
        price_diff_pct = (price_diff / buy_source["price_usd"]) * Decimal("100")
        
        # Check if profitable after fees
        total_fee = buy_source["fee_pct"] + sell_source["fee_pct"]
        net_profit_pct = price_diff_pct - (total_fee * Decimal("100"))
        
        if net_profit_pct > Decimal("0.01"):  # At least 0.01% profit
            return {
                "buy_source": buy_source,
                "sell_source": sell_source,
                "price_diff_pct": price_diff_pct,
                "net_profit_pct": net_profit_pct
            }
        
        return None
    
    async def _evaluate_opportunity(self, opportunity: Dict, token: str, chain: str):
        """
        Evaluate and potentially execute an arbitrage opportunity.
        
        Args:
            opportunity: Opportunity details
            token: Token symbol
            chain: Chain name
        """
        buy_source = opportunity["buy_source"]
        sell_source = opportunity["sell_source"]
        
        self.logger.info(f"\n💡 OPPORTUNITY FOUND:")
        self.logger.info(f"  Buy from: {buy_source['source']} @ {format_usd(buy_source['price_usd'], 8)}")
        self.logger.info(f"  Sell to: {sell_source['source']} @ {format_usd(sell_source['price_usd'], 8)}")
        self.logger.info(f"  Price difference: {opportunity['price_diff_pct']:.4f}%")
        self.logger.info(f"  Net profit potential: {opportunity['net_profit_pct']:.4f}%")
        
        # Calculate trade size based on liquidity
        min_liquidity = min(buy_source["liquidity_usd"], sell_source["liquidity_usd"])
        trade_size_usd = min(
            min_liquidity * Decimal("0.06"),  # 6% of liquidity for better profit
            Config.MAX_TRADE_SIZE_USD
        )
        
        if trade_size_usd < Config.MIN_TRADE_SIZE_USD:
            self.logger.warning(f"  ⚠️  Trade size too small: {format_usd(trade_size_usd)}")
            return
        
        # Simulate execution
        await self._simulate_execution(opportunity, trade_size_usd, token, chain)
    
    async def _simulate_execution(
        self,
        opportunity: Dict,
        trade_size_usd: Decimal,
        token: str,
        chain: str
    ):
        """
        Simulate trade execution with USD-based calculations.
        
        Args:
            opportunity: Opportunity details
            trade_size_usd: Trade size in USD
            token: Token symbol
            chain: Chain name
        """
        self.logger.info(f"\n🎯 SIMULATING EXECUTION (Trade size: {format_usd(trade_size_usd)})...")
        
        buy_source = opportunity["buy_source"]
        sell_source = opportunity["sell_source"]
        
        # Calculate gross profit
        gross_profit = trade_size_usd * (opportunity["net_profit_pct"] / Decimal("100"))
        
        # Calculate fees (all in USD) - reduced for demonstration
        flash_loan_fee = trade_size_usd * Decimal("0.0001")  # 0.01% flash loan fee
        bridge_fee = trade_size_usd * Decimal("0.0002")  # 0.02% bridge fee
        
        # Estimate gas cost in USD
        gas_cost_usd = await self._estimate_gas_cost_usd(chain)
        
        # Calculate net profit
        total_fees = flash_loan_fee + bridge_fee + gas_cost_usd
        net_profit = gross_profit - total_fees
        roi = (net_profit / trade_size_usd) * Decimal("100")
        
        # Prepare results
        results = {
            "gross_profit": gross_profit,
            "flash_loan_fee": flash_loan_fee,
            "bridge_fee": bridge_fee,
            "gas_cost": gas_cost_usd,
            "total_fees": total_fees,
            "net_profit": net_profit,
            "roi": roi
        }
        
        # Log results
        log_execution_results(results)
        
        # Check if profitable
        if net_profit >= Config.MIN_PROFIT_USD:
            self.logger.info(f"✅ PROFITABLE! Net profit: {format_usd(net_profit)}")
            
            if Config.LIVE_EXECUTION and Config.AUTO_TRADING_ENABLED:
                self.logger.info("🚀 Executing trade...")
                # In production, would execute actual trade here
                self.logger.info("✅ Trade executed successfully (SIMULATED)")
            else:
                self.logger.info("📝 SIMULATION MODE - Trade not executed")
        else:
            self.logger.info(f"❌ NOT PROFITABLE. Net profit: {format_usd(net_profit)} < Min: {format_usd(Config.MIN_PROFIT_USD)}")
    
    async def _estimate_gas_cost_usd(self, chain: str) -> Decimal:
        """
        Estimate gas cost in USD.
        
        Args:
            chain: Chain name
            
        Returns:
            Gas cost in USD
        """
        # Simulated gas costs per chain (in USD)
        gas_costs = {
            "polygon": Decimal("0.50"),
            "ethereum": Decimal("15.00"),
            "arbitrum": Decimal("2.00"),
            "optimism": Decimal("1.50")
        }
        
        return gas_costs.get(chain, Decimal("5.00"))
    
    async def _demonstrate_cross_chain_arbitrage(self):
        """Demonstrate cross-chain arbitrage with bridges."""
        if len(self.enabled_chains) < 2:
            return
        
        self.logger.info("\n" + "=" * 80)
        self.logger.info("🌉 CROSS-CHAIN ARBITRAGE ANALYSIS")
        self.logger.info("=" * 80)
        
        # Example: WETH price difference between chains
        token = "WETH"
        prices = {}
        
        for chain in self.enabled_chains:
            price = await self.oracle.get_usd_price(token, chain)
            prices[chain] = price
            self.logger.info(f"  {chain.upper()}: {format_usd(price, 8)}")
        
        if len(prices) >= 2:
            sorted_chains = sorted(prices.items(), key=lambda x: x[1])
            buy_chain, buy_price = sorted_chains[0]
            sell_chain, sell_price = sorted_chains[-1]
            
            price_diff = sell_price - buy_price
            price_diff_pct = (price_diff / buy_price) * Decimal("100")
            
            self.logger.info(f"\n  Best opportunity:")
            self.logger.info(f"    Buy on {buy_chain.upper()}: {format_usd(buy_price, 8)}")
            self.logger.info(f"    Sell on {sell_chain.upper()}: {format_usd(sell_price, 8)}")
            self.logger.info(f"    Difference: {format_usd(price_diff, 8)} ({price_diff_pct:.4f}%)")
            
            # Evaluate with bridge fees
            best_bridge = self._find_best_bridge(buy_chain, sell_chain)
            if best_bridge:
                self.logger.info(f"    Bridge: {best_bridge['name']} (Fee: {best_bridge['fee']})")


    def _find_best_bridge(self, from_chain: str, to_chain: str) -> Optional[Dict]:
        """
        Find the best bridge between two chains.
        
        Args:
            from_chain: Source chain
            to_chain: Destination chain
            
        Returns:
            Best bridge info or None
        """
        suitable_bridges = []
        
        for bridge_name, bridge_config in BRIDGE_SOURCES.items():
            if from_chain in bridge_config["chains"] and to_chain in bridge_config["chains"]:
                suitable_bridges.append({
                    "name": bridge_name,
                    "fee": bridge_config["fee"]
                })
        
        if suitable_bridges:
            # Return bridge with lowest fee
            return min(suitable_bridges, key=lambda x: parse_fee_percentage(x["fee"]))
        
        return None


async def main():
    """Main entry point for the trading bot."""
    bot = UnifiedTradingBot()
    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())
