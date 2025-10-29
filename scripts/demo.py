#!/usr/bin/env python3
"""
Demo script to showcase terminal output features
Runs the bot for a few cycles to demonstrate the colored output
"""
import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.bot import UnifiedTradingBot


async def demo():
    """Run demo for a limited number of cycles"""
    print("\n" + "="*84)
    print("TRADING BOT TERMINAL OUTPUT DEMO".center(84))
    print("="*84 + "\n")
    
    print("This demo will run 3-5 bot cycles to showcase:")
    print("  • Color-coded terminal output")
    print("  • Price comparison tables")
    print("  • Execution results")
    print("  • Trading statistics")
    print("  • Bot cycle displays")
    print("\nStarting in 2 seconds...\n")
    
    await asyncio.sleep(2)
    
    # Create bot instance
    bot = UnifiedTradingBot()
    
    # Run a few cycles
    max_cycles = 5
    for i in range(max_cycles):
        await bot.run_cycle()
        
        # Wait between cycles
        if i < max_cycles - 1:
            await asyncio.sleep(2)
    
    # Display final statistics
    print("\n" + "="*84)
    print("DEMO COMPLETE".center(84))
    print("="*84 + "\n")
    
    if bot.stats.total_trades > 0:
        bot.display_statistics()


if __name__ == "__main__":
    asyncio.run(demo())
