"""Strategy selection using Factory pattern.

This module implements the Strategy
to dynamically select the optimal algorithm based on input characteristics.
"""
from __future__ import annotations

import math

from knight_journey.domain import Cell
from ..strategy import KillingStrategy
from ..strategies import BucketsStrategy, HeapStrategy
from ..config import StrategyConfig

class StrategySelector:
    """Factory for selecting optimal killing strategy.
    
    Implements the Factory pattern to choose between:
    - HeapStrategy: O(n log n) - Better for large gold values
    - BucketsStrategy: O(n + G) - Better for small gold values
    
    This is an example of the Strategy pattern where the algorithm
    is selected at runtime based on input characteristics.
    """
    
    def __init__(self, n: int, max_gold: int) -> None:
        """Initialize selector with problem characteristics.
        
        Args:
            n: Number of cells/board size
            max_gold: Maximum gold value among all dragons
        """
        self.n = n
        self.max_gold = max_gold

    def choose(self) -> KillingStrategy:
        """Select optimal strategy based on complexity analysis.
        
        Returns:
            KillingStrategy instance (either HeapStrategy or BucketsStrategy)
        """
        nlogn = self.n * math.log2(max(2, self.n))
        linear = self.n + self.max_gold
        
        # Choose heap if its complexity is significantly better
        if nlogn < linear * StrategyConfig.HEAP_THRESHOLD_MULTIPLIER:
            return HeapStrategy(last_index=self.n)
        return BucketsStrategy(max_gold=self.max_gold, last_index=self.n)

def select_strategy(*, n: int, cells: list[Cell]) -> KillingStrategy:
    return StrategySelector.choose(n=n, cells=cells)

__all__ = ["StrategySelector", "select_strategy"]
