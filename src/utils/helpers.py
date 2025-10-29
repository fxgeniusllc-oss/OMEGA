"""Helper utility functions."""
import asyncio
from typing import List, Dict, Any
from datetime import datetime
import math


def calculate_kelly_fraction(win_probability: float, win_loss_ratio: float, max_fraction: float = 0.25) -> float:
    """
    Calculate Kelly Criterion position size.
    
    Args:
        win_probability: Probability of winning (0-1)
        win_loss_ratio: Ratio of win amount to loss amount
        max_fraction: Maximum fraction to risk (default 0.25 for conservative approach)
    
    Returns:
        Position size as a fraction of capital
    """
    if win_probability <= 0 or win_probability >= 1:
        return 0.0
    
    if win_loss_ratio <= 0:
        return 0.0
    
    # Kelly formula: f = (p * b - q) / b
    # where p = win probability, q = loss probability, b = win/loss ratio
    loss_probability = 1 - win_probability
    kelly_fraction = (win_probability * win_loss_ratio - loss_probability) / win_loss_ratio
    
    # Cap at max fraction for risk management
    return max(0.0, min(kelly_fraction, max_fraction))


def calculate_position_size(
    capital: float,
    win_probability: float,
    expected_profit: float,
    expected_loss: float,
    max_position: float
) -> float:
    """
    Calculate optimal position size using Kelly Criterion.
    
    Args:
        capital: Available capital
        win_probability: Probability of success
        expected_profit: Expected profit amount
        expected_loss: Expected loss amount
        max_position: Maximum position size limit
    
    Returns:
        Recommended position size
    """
    if expected_loss <= 0:
        return 0.0
    
    win_loss_ratio = expected_profit / expected_loss
    kelly_frac = calculate_kelly_fraction(win_probability, win_loss_ratio)
    
    position_size = capital * kelly_frac
    
    # Apply maximum position limit
    return min(position_size, max_position)


def calculate_slippage_impact(amount: float, liquidity: float, slippage_tolerance: float = 0.005) -> float:
    """
    Estimate slippage impact on trade.
    
    Args:
        amount: Trade amount
        liquidity: Available liquidity
        slippage_tolerance: Maximum acceptable slippage
    
    Returns:
        Estimated slippage as a fraction
    """
    if liquidity <= 0:
        return 1.0  # 100% slippage if no liquidity
    
    # Simplified slippage model: quadratic function
    impact_ratio = amount / liquidity
    slippage = impact_ratio ** 2
    
    return min(slippage, slippage_tolerance)


def calculate_profit_after_fees(
    gross_profit: float,
    gas_cost: float,
    flash_loan_fee: float = 0.0
) -> float:
    """
    Calculate net profit after all fees.
    
    Args:
        gross_profit: Profit before fees
        gas_cost: Gas cost in USD
        flash_loan_fee: Flash loan fee if applicable
    
    Returns:
        Net profit
    """
    return gross_profit - gas_cost - flash_loan_fee


def rank_opportunities(opportunities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Rank trading opportunities by profit * confidence.
    
    Args:
        opportunities: List of opportunity dictionaries
    
    Returns:
        Sorted list of opportunities
    """
    for opp in opportunities:
        score = opp.get('profit', 0) * opp.get('confidence', 0)
        opp['score'] = score
    
    return sorted(opportunities, key=lambda x: x.get('score', 0), reverse=True)


def validate_transaction_params(
    amount: float,
    slippage: float,
    gas_price: int,
    max_position: float
) -> tuple[bool, str]:
    """
    Validate transaction parameters.
    
    Args:
        amount: Transaction amount
        slippage: Slippage tolerance
        gas_price: Gas price
        max_position: Maximum position size
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if amount <= 0:
        return False, "Amount must be positive"
    
    if amount > max_position:
        return False, f"Amount exceeds max position size: {max_position}"
    
    if slippage < 0 or slippage > 0.1:
        return False, "Slippage must be between 0 and 0.1 (10%)"
    
    if gas_price <= 0:
        return False, "Gas price must be positive"
    
    return True, ""


async def retry_async(func, max_retries: int = 3, delay: float = 1.0):
    """
    Retry an async function with exponential backoff.
    
    Args:
        func: Async function to retry
        max_retries: Maximum number of retries
        delay: Initial delay between retries
    
    Returns:
        Result of function or None if all retries fail
    """
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"All retries failed: {e}")
                return None
            await asyncio.sleep(delay * (2 ** attempt))
    return None
