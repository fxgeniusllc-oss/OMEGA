"""Utility helper functions for the DeFi Trading Bot."""

from decimal import Decimal
from typing import Optional


def format_usd(amount: Decimal, decimals: int = 2) -> str:
    """
    Format a Decimal amount as USD string.
    
    Args:
        amount: The amount to format
        decimals: Number of decimal places (default 2)
        
    Returns:
        Formatted string like "$1,234.56 USD"
    """
    if amount is None:
        return "$0.00 USD"
    
    amount_str = f"{amount:,.{decimals}f}"
    return f"${amount_str}"


def format_usd_with_label(amount: Decimal, decimals: int = 2) -> str:
    """
    Format a Decimal amount as USD string with USD label.
    
    Args:
        amount: The amount to format
        decimals: Number of decimal places (default 2)
        
    Returns:
        Formatted string like "$1,234.56 USD"
    """
    return f"{format_usd(amount, decimals)} USD"


def parse_fee_percentage(fee_str: str) -> Decimal:
    """
    Parse a fee percentage string like "0.03%" to Decimal.
    
    Args:
        fee_str: Fee string like "0.03%"
        
    Returns:
        Decimal representation (e.g., 0.0003 for 0.03%)
    """
    fee_str = fee_str.replace("%", "").strip()
    return Decimal(fee_str) / Decimal("100")


def calculate_percentage_change(old_value: Decimal, new_value: Decimal) -> Decimal:
    """
    Calculate percentage change between two values.
    
    Args:
        old_value: Original value
        new_value: New value
        
    Returns:
        Percentage change as Decimal
    """
    if old_value == 0:
        return Decimal("0")
    
    return ((new_value - old_value) / old_value) * Decimal("100")


def safe_decimal(value: any, default: Decimal = Decimal("0")) -> Decimal:
    """
    Safely convert a value to Decimal.
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
        
    Returns:
        Decimal value
    """
    if isinstance(value, Decimal):
        return value
    
    try:
        return Decimal(str(value))
    except (ValueError, TypeError, Exception):
        return default
