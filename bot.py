"""
Convenience wrapper to run the bot directly.
You can also run: python -m src.bot
"""
from src.bot import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())
