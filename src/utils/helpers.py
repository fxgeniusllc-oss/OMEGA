"""
Utility helper functions
"""
from decimal import Decimal
from typing import Optional

def wei_to_ether(wei_amount: int) -> Decimal:
    """Convert wei to ether"""
    return Decimal(wei_amount) / Decimal(10**18)

def ether_to_wei(ether_amount: float) -> int:
    """Convert ether to wei"""
    return int(Decimal(str(ether_amount)) * Decimal(10**18))

def format_address(address: str) -> str:
    """Format Ethereum address for display"""
    if not address:
        return "N/A"
    return f"{address[:6]}...{address[-4:]}"

def format_usd(amount: float) -> str:
    """Format USD amount for display"""
    if amount >= 1_000_000:
        return f"${amount/1_000_000:.2f}M"
    elif amount >= 1_000:
        return f"${amount/1_000:.2f}K"
    else:
        return f"${amount:.2f}"

def bps_to_percent(bps: int) -> float:
    """Convert basis points to percentage"""
    return bps / 100.0

def calculate_slippage(amount: Decimal, slippage_bps: int) -> Decimal:
    """Calculate slippage amount"""
    return amount * Decimal(slippage_bps) / Decimal(10000)

def safe_div(a: float, b: float, default: float = 0.0) -> float:
    """Safe division with default value"""
    try:
        return a / b if b != 0 else default
    except (ZeroDivisionError, TypeError):
        return default
