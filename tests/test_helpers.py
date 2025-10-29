"""Tests for helper functions."""

import pytest
from decimal import Decimal
from src.utils.helpers import (
    format_usd,
    format_usd_with_label,
    parse_fee_percentage,
    calculate_percentage_change,
    safe_decimal
)


def test_format_usd():
    """Test USD formatting."""
    # Test basic formatting
    amount = Decimal("1234.56")
    formatted = format_usd(amount)
    assert formatted == "$1,234.56"
    
    # Test with different decimal places
    amount = Decimal("1234.567890")
    formatted = format_usd(amount, decimals=4)
    assert formatted == "$1,234.5679"
    
    # Test with None
    formatted = format_usd(None)
    assert formatted == "$0.00 USD"


def test_format_usd_with_label():
    """Test USD formatting with label."""
    amount = Decimal("1234.56")
    formatted = format_usd_with_label(amount)
    assert formatted == "$1,234.56 USD"


def test_parse_fee_percentage():
    """Test parsing fee percentages."""
    # Test standard percentage
    fee = parse_fee_percentage("0.03%")
    assert fee == Decimal("0.0003")
    
    # Test different percentage
    fee = parse_fee_percentage("0.5%")
    assert fee == Decimal("0.005")
    
    # Test without percent sign
    fee = parse_fee_percentage("0.1")
    assert fee == Decimal("0.001")


def test_calculate_percentage_change():
    """Test percentage change calculation."""
    # Test increase
    old_value = Decimal("100")
    new_value = Decimal("110")
    change = calculate_percentage_change(old_value, new_value)
    assert change == Decimal("10")
    
    # Test decrease
    old_value = Decimal("100")
    new_value = Decimal("90")
    change = calculate_percentage_change(old_value, new_value)
    assert change == Decimal("-10")
    
    # Test no change
    old_value = Decimal("100")
    new_value = Decimal("100")
    change = calculate_percentage_change(old_value, new_value)
    assert change == Decimal("0")
    
    # Test with zero old value
    old_value = Decimal("0")
    new_value = Decimal("100")
    change = calculate_percentage_change(old_value, new_value)
    assert change == Decimal("0")


def test_safe_decimal():
    """Test safe decimal conversion."""
    # Test with Decimal
    value = Decimal("123.45")
    result = safe_decimal(value)
    assert result == Decimal("123.45")
    
    # Test with string
    value = "123.45"
    result = safe_decimal(value)
    assert result == Decimal("123.45")
    
    # Test with int
    value = 123
    result = safe_decimal(value)
    assert result == Decimal("123")
    
    # Test with float
    value = 123.45
    result = safe_decimal(value)
    assert result == Decimal("123.45")
    
    # Test with invalid value
    value = "invalid"
    result = safe_decimal(value)
    assert result == Decimal("0")
    
    # Test with None
    value = None
    result = safe_decimal(value)
    assert result == Decimal("0")
    
    # Test with custom default
    value = "invalid"
    result = safe_decimal(value, default=Decimal("100"))
    assert result == Decimal("100")
