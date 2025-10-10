"""Configuration constants for Knight Journey application.

This module centralizes all configuration values to follow the
Single Responsibility Principle and make the codebase more maintainable.
"""

from __future__ import annotations


class ValidationConfig:
    """Validation constraints for input data."""
    
    # Dragon gold constraints
    MIN_GOLD = 0
    MAX_GOLD = 10_000_000
    
    # Princess beauty constraints
    MIN_BEAUTY_MID = 1
    MAX_BEAUTY_MID = 200_000
    MIN_BEAUTY_LAST = 0
    MAX_BEAUTY_LAST = 200_000
    
    # Board size constraints
    MIN_BOARD_SIZE = 1
    MAX_BOARD_SIZE = 1_000_000


class StrategyConfig:
    """Configuration for strategy selection algorithm."""
    
    # Threshold multiplier for choosing between heap and buckets strategy
    # heap complexity: O(n log n)
    # buckets complexity: O(n + G)
    # We choose heap if: n*log(n) < (n + G) * THRESHOLD
    HEAP_THRESHOLD_MULTIPLIER = 0.9


class OutputConfig:
    """Configuration for output formatting."""
    
    ERROR_EXIT_VALUE = -1
    SUCCESS_EXIT_CODE = 0


__all__ = [
    "ValidationConfig",
    "StrategyConfig",
    "OutputConfig",
]


