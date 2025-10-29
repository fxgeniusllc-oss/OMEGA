"""
Retry utilities with exponential backoff for API calls and blockchain operations.

This module provides decorators and utilities for handling transient failures
in API calls with configurable retry logic and exponential backoff.
"""

import asyncio
import logging
import time
import functools
from typing import Callable, Optional, Type, Tuple, Union
from enum import Enum

logger = logging.getLogger(__name__)


class RetryError(Exception):
    """Exception raised when all retry attempts are exhausted."""
    pass


class ErrorType(Enum):
    """Types of errors that can trigger retries."""
    RATE_LIMIT = "rate_limit"
    NETWORK = "network"
    TIMEOUT = "timeout"
    SERVER_ERROR = "server_error"
    UNKNOWN = "unknown"


def is_retryable_error(error: Exception) -> Tuple[bool, ErrorType]:
    """
    Determine if an error is retryable and classify it.
    
    Args:
        error: The exception to check
        
    Returns:
        Tuple of (is_retryable, error_type)
    """
    error_str = str(error).lower()
    error_type_name = type(error).__name__.lower()
    
    # Rate limiting errors (check first, most specific)
    if any(x in error_str for x in ['rate limit', 'too many requests', '429']):
        return True, ErrorType.RATE_LIMIT
    
    # Timeout errors (check before network errors since TimeoutError is more specific)
    if 'timeout' in error_str or 'timeouterror' in error_type_name:
        return True, ErrorType.TIMEOUT
    
    # Network errors
    if any(x in error_type_name for x in ['connectionerror', 'httperror']):
        return True, ErrorType.NETWORK
    
    # Server errors (5xx)
    if any(x in error_str for x in ['500', '502', '503', '504', 'server error']):
        return True, ErrorType.SERVER_ERROR
    
    # Unknown but potentially retryable
    return False, ErrorType.UNKNOWN


def calculate_backoff(
    attempt: int,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True
) -> float:
    """
    Calculate exponential backoff delay with optional jitter.
    
    Args:
        attempt: Current attempt number (0-indexed)
        base_delay: Base delay in seconds
        max_delay: Maximum delay in seconds
        exponential_base: Base for exponential calculation
        jitter: Whether to add random jitter to prevent thundering herd
        
    Returns:
        Delay in seconds
    """
    import random
    
    # Calculate exponential backoff: base_delay * (exponential_base ^ attempt)
    delay = min(base_delay * (exponential_base ** attempt), max_delay)
    
    # Add jitter: random value between 0 and delay
    if jitter:
        delay = random.uniform(0, delay)
    
    return delay


def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    retryable_exceptions: Optional[Tuple[Type[Exception], ...]] = None,
    on_retry: Optional[Callable] = None
):
    """
    Decorator for synchronous functions that adds retry logic with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds
        max_delay: Maximum delay in seconds
        exponential_base: Base for exponential calculation (default 2.0)
        jitter: Whether to add random jitter
        retryable_exceptions: Tuple of exception types to retry
        on_retry: Optional callback function called on each retry
        
    Example:
        @retry_with_backoff(max_retries=3, base_delay=1.0)
        def fetch_data():
            # Your code here
            pass
    """
    if retryable_exceptions is None:
        retryable_exceptions = (Exception,)
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                    
                except retryable_exceptions as e:
                    last_exception = e
                    
                    # Check if error is retryable
                    is_retry, error_type = is_retryable_error(e)
                    
                    # If not retryable, raise immediately
                    if not is_retry:
                        logger.warning(
                            f"{func.__name__}: Non-retryable error: {type(e).__name__}: {e}"
                        )
                        raise
                    
                    # If last attempt, break to raise RetryError
                    if attempt >= max_retries:
                        break
                    
                    # Calculate backoff delay
                    delay = calculate_backoff(
                        attempt,
                        base_delay=base_delay,
                        max_delay=max_delay,
                        exponential_base=exponential_base,
                        jitter=jitter
                    )
                    
                    logger.warning(
                        f"{func.__name__}: Attempt {attempt + 1}/{max_retries + 1} failed "
                        f"with {error_type.value}: {type(e).__name__}: {e}. "
                        f"Retrying in {delay:.2f}s..."
                    )
                    
                    # Call retry callback if provided
                    if on_retry:
                        on_retry(attempt, e, delay)
                    
                    # Wait before retrying
                    time.sleep(delay)
            
            # If we get here, all retries failed
            raise RetryError(
                f"{func.__name__}: All {max_retries + 1} attempts failed. "
                f"Last error: {type(last_exception).__name__}: {last_exception}"
            ) from last_exception
        
        return wrapper
    return decorator


def async_retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    retryable_exceptions: Optional[Tuple[Type[Exception], ...]] = None,
    on_retry: Optional[Callable] = None
):
    """
    Decorator for async functions that adds retry logic with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds
        max_delay: Maximum delay in seconds
        exponential_base: Base for exponential calculation (default 2.0)
        jitter: Whether to add random jitter
        retryable_exceptions: Tuple of exception types to retry
        on_retry: Optional callback function called on each retry
        
    Example:
        @async_retry_with_backoff(max_retries=3, base_delay=1.0)
        async def fetch_data():
            # Your async code here
            pass
    """
    if retryable_exceptions is None:
        retryable_exceptions = (Exception,)
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                    
                except retryable_exceptions as e:
                    last_exception = e
                    
                    # Check if error is retryable
                    is_retry, error_type = is_retryable_error(e)
                    
                    # If not retryable, raise immediately
                    if not is_retry:
                        logger.warning(
                            f"{func.__name__}: Non-retryable error: {type(e).__name__}: {e}"
                        )
                        raise
                    
                    # If last attempt, break to raise RetryError
                    if attempt >= max_retries:
                        break
                    
                    # Calculate backoff delay
                    delay = calculate_backoff(
                        attempt,
                        base_delay=base_delay,
                        max_delay=max_delay,
                        exponential_base=exponential_base,
                        jitter=jitter
                    )
                    
                    logger.warning(
                        f"{func.__name__}: Attempt {attempt + 1}/{max_retries + 1} failed "
                        f"with {error_type.value}: {type(e).__name__}: {e}. "
                        f"Retrying in {delay:.2f}s..."
                    )
                    
                    # Call retry callback if provided
                    if on_retry:
                        if asyncio.iscoroutinefunction(on_retry):
                            await on_retry(attempt, e, delay)
                        else:
                            on_retry(attempt, e, delay)
                    
                    # Wait before retrying
                    await asyncio.sleep(delay)
            
            # If we get here, all retries failed
            raise RetryError(
                f"{func.__name__}: All {max_retries + 1} attempts failed. "
                f"Last error: {type(last_exception).__name__}: {last_exception}"
            ) from last_exception
        
        return wrapper
    return decorator


class RetryConfig:
    """Configuration for retry behavior."""
    
    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        jitter: bool = True
    ):
        """
        Initialize retry configuration.
        
        Args:
            max_retries: Maximum number of retry attempts
            base_delay: Base delay in seconds
            max_delay: Maximum delay in seconds
            exponential_base: Base for exponential calculation
            jitter: Whether to add random jitter
        """
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter
    
    @classmethod
    def from_env(cls) -> 'RetryConfig':
        """Create RetryConfig from environment variables."""
        import os
        
        return cls(
            max_retries=int(os.getenv('RETRY_MAX_ATTEMPTS', '3')),
            base_delay=float(os.getenv('RETRY_BASE_DELAY', '1.0')),
            max_delay=float(os.getenv('RETRY_MAX_DELAY', '60.0')),
            exponential_base=float(os.getenv('RETRY_EXPONENTIAL_BASE', '2.0')),
            jitter=os.getenv('RETRY_JITTER', 'true').lower() == 'true'
        )
    
    def to_dict(self):
        """Convert config to dictionary."""
        return {
            'max_retries': self.max_retries,
            'base_delay': self.base_delay,
            'max_delay': self.max_delay,
            'exponential_base': self.exponential_base,
            'jitter': self.jitter
        }
