"""Tests for retry utilities with exponential backoff."""

import pytest
import asyncio
import time
from unittest.mock import Mock, patch
from src.utils.retry import (
    retry_with_backoff,
    async_retry_with_backoff,
    calculate_backoff,
    is_retryable_error,
    RetryError,
    ErrorType,
    RetryConfig
)


class TestCalculateBackoff:
    """Test exponential backoff calculation."""
    
    def test_basic_exponential_backoff(self):
        """Test basic exponential backoff without jitter."""
        # Test exponential growth
        delay0 = calculate_backoff(0, base_delay=1.0, jitter=False)
        delay1 = calculate_backoff(1, base_delay=1.0, jitter=False)
        delay2 = calculate_backoff(2, base_delay=1.0, jitter=False)
        
        assert delay0 == 1.0  # 1.0 * 2^0 = 1.0
        assert delay1 == 2.0  # 1.0 * 2^1 = 2.0
        assert delay2 == 4.0  # 1.0 * 2^2 = 4.0
    
    def test_max_delay_cap(self):
        """Test that delay is capped at max_delay."""
        delay = calculate_backoff(10, base_delay=1.0, max_delay=10.0, jitter=False)
        assert delay == 10.0  # Should be capped at max_delay
    
    def test_jitter_adds_randomness(self):
        """Test that jitter adds randomness to delay."""
        delays = [calculate_backoff(2, base_delay=1.0, jitter=True) for _ in range(10)]
        
        # All delays should be between 0 and 4.0
        assert all(0 <= d <= 4.0 for d in delays)
        
        # Delays should vary (not all the same)
        assert len(set(delays)) > 1


class TestIsRetryableError:
    """Test error classification."""
    
    def test_rate_limit_error(self):
        """Test rate limit error detection."""
        error = Exception("Rate limit exceeded")
        is_retryable, error_type = is_retryable_error(error)
        
        assert is_retryable is True
        assert error_type == ErrorType.RATE_LIMIT
    
    def test_429_error(self):
        """Test HTTP 429 error detection."""
        error = Exception("HTTP 429: Too many requests")
        is_retryable, error_type = is_retryable_error(error)
        
        assert is_retryable is True
        assert error_type == ErrorType.RATE_LIMIT
    
    def test_timeout_error(self):
        """Test timeout error detection."""
        error = TimeoutError("Connection timed out")
        is_retryable, error_type = is_retryable_error(error)
        
        assert is_retryable is True
        assert error_type == ErrorType.TIMEOUT
    
    def test_server_error(self):
        """Test server error detection."""
        error = Exception("HTTP 503: Service unavailable")
        is_retryable, error_type = is_retryable_error(error)
        
        assert is_retryable is True
        assert error_type == ErrorType.SERVER_ERROR
    
    def test_non_retryable_error(self):
        """Test non-retryable error."""
        error = ValueError("Invalid input")
        is_retryable, error_type = is_retryable_error(error)
        
        assert is_retryable is False
        assert error_type == ErrorType.UNKNOWN


class TestRetryWithBackoff:
    """Test synchronous retry decorator."""
    
    def test_successful_first_attempt(self):
        """Test function succeeds on first attempt."""
        call_count = [0]
        
        @retry_with_backoff(max_retries=3)
        def successful_func():
            call_count[0] += 1
            return "success"
        
        result = successful_func()
        
        assert result == "success"
        assert call_count[0] == 1
    
    def test_retry_on_rate_limit(self):
        """Test retry on rate limit error."""
        call_count = [0]
        
        @retry_with_backoff(max_retries=3, base_delay=0.01)
        def rate_limited_func():
            call_count[0] += 1
            if call_count[0] < 3:
                raise Exception("Rate limit exceeded")
            return "success"
        
        result = rate_limited_func()
        
        assert result == "success"
        assert call_count[0] == 3
    
    def test_all_retries_exhausted(self):
        """Test that RetryError is raised when all retries fail."""
        call_count = [0]
        
        @retry_with_backoff(max_retries=2, base_delay=0.01)
        def always_fails():
            call_count[0] += 1
            raise Exception("Rate limit exceeded")
        
        with pytest.raises(RetryError) as exc_info:
            always_fails()
        
        assert call_count[0] == 3  # Initial + 2 retries
        assert "All 3 attempts failed" in str(exc_info.value)
    
    def test_non_retryable_error_not_retried(self):
        """Test that non-retryable errors are not retried."""
        call_count = [0]
        
        @retry_with_backoff(max_retries=3, base_delay=0.01)
        def non_retryable_error():
            call_count[0] += 1
            raise ValueError("Invalid input")
        
        with pytest.raises(ValueError):
            non_retryable_error()
        
        assert call_count[0] == 1  # Should not retry
    
    def test_on_retry_callback(self):
        """Test that on_retry callback is called."""
        call_count = [0]
        retry_calls = []
        
        def on_retry_callback(attempt, error, delay):
            retry_calls.append((attempt, type(error).__name__, delay))
        
        @retry_with_backoff(max_retries=2, base_delay=0.01, on_retry=on_retry_callback)
        def failing_func():
            call_count[0] += 1
            if call_count[0] < 3:
                raise Exception("Rate limit exceeded")
            return "success"
        
        result = failing_func()
        
        assert result == "success"
        assert len(retry_calls) == 2
        assert all(attempt in [0, 1] for attempt, _, _ in retry_calls)


@pytest.mark.asyncio
class TestAsyncRetryWithBackoff:
    """Test asynchronous retry decorator."""
    
    async def test_successful_first_attempt(self):
        """Test async function succeeds on first attempt."""
        call_count = [0]
        
        @async_retry_with_backoff(max_retries=3)
        async def successful_async_func():
            call_count[0] += 1
            return "success"
        
        result = await successful_async_func()
        
        assert result == "success"
        assert call_count[0] == 1
    
    async def test_retry_on_rate_limit(self):
        """Test async retry on rate limit error."""
        call_count = [0]
        
        @async_retry_with_backoff(max_retries=3, base_delay=0.01)
        async def rate_limited_async_func():
            call_count[0] += 1
            if call_count[0] < 3:
                raise Exception("Rate limit exceeded")
            return "success"
        
        result = await rate_limited_async_func()
        
        assert result == "success"
        assert call_count[0] == 3
    
    async def test_all_retries_exhausted(self):
        """Test that RetryError is raised when all async retries fail."""
        call_count = [0]
        
        @async_retry_with_backoff(max_retries=2, base_delay=0.01)
        async def always_fails_async():
            call_count[0] += 1
            raise Exception("Rate limit exceeded")
        
        with pytest.raises(RetryError) as exc_info:
            await always_fails_async()
        
        assert call_count[0] == 3  # Initial + 2 retries
        assert "All 3 attempts failed" in str(exc_info.value)
    
    async def test_exponential_backoff_timing(self):
        """Test that async backoff timing is correct."""
        call_count = [0]
        times = []
        
        @async_retry_with_backoff(max_retries=3, base_delay=0.1, jitter=False)
        async def timed_func():
            times.append(time.time())
            call_count[0] += 1
            if call_count[0] < 3:
                raise Exception("Rate limit exceeded")
            return "success"
        
        start_time = time.time()
        result = await timed_func()
        total_time = time.time() - start_time
        
        assert result == "success"
        assert call_count[0] == 3
        
        # Total wait time should be approximately 0.1 + 0.2 = 0.3 seconds
        # Allow some tolerance for execution time
        assert 0.25 < total_time < 0.45
    
    async def test_async_on_retry_callback(self):
        """Test that async on_retry callback is called."""
        call_count = [0]
        retry_calls = []
        
        async def async_on_retry_callback(attempt, error, delay):
            retry_calls.append((attempt, type(error).__name__, delay))
        
        @async_retry_with_backoff(
            max_retries=2, 
            base_delay=0.01, 
            on_retry=async_on_retry_callback
        )
        async def failing_async_func():
            call_count[0] += 1
            if call_count[0] < 3:
                raise Exception("Rate limit exceeded")
            return "success"
        
        result = await failing_async_func()
        
        assert result == "success"
        assert len(retry_calls) == 2


class TestRetryConfig:
    """Test RetryConfig class."""
    
    def test_default_config(self):
        """Test default configuration."""
        config = RetryConfig()
        
        assert config.max_retries == 3
        assert config.base_delay == 1.0
        assert config.max_delay == 60.0
        assert config.exponential_base == 2.0
        assert config.jitter is True
    
    def test_custom_config(self):
        """Test custom configuration."""
        config = RetryConfig(
            max_retries=5,
            base_delay=2.0,
            max_delay=120.0,
            exponential_base=3.0,
            jitter=False
        )
        
        assert config.max_retries == 5
        assert config.base_delay == 2.0
        assert config.max_delay == 120.0
        assert config.exponential_base == 3.0
        assert config.jitter is False
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        config = RetryConfig(max_retries=5, base_delay=2.0)
        config_dict = config.to_dict()
        
        assert config_dict['max_retries'] == 5
        assert config_dict['base_delay'] == 2.0
        assert 'max_delay' in config_dict
        assert 'exponential_base' in config_dict
        assert 'jitter' in config_dict
    
    @patch.dict('os.environ', {
        'RETRY_MAX_ATTEMPTS': '5',
        'RETRY_BASE_DELAY': '2.0',
        'RETRY_MAX_DELAY': '120.0',
        'RETRY_EXPONENTIAL_BASE': '3.0',
        'RETRY_JITTER': 'false'
    })
    def test_from_env(self):
        """Test loading configuration from environment variables."""
        config = RetryConfig.from_env()
        
        assert config.max_retries == 5
        assert config.base_delay == 2.0
        assert config.max_delay == 120.0
        assert config.exponential_base == 3.0
        assert config.jitter is False
    
    @patch.dict('os.environ', {}, clear=True)
    def test_from_env_defaults(self):
        """Test loading configuration with default values."""
        config = RetryConfig.from_env()
        
        assert config.max_retries == 3
        assert config.base_delay == 1.0
        assert config.max_delay == 60.0
        assert config.exponential_base == 2.0
        assert config.jitter is True
