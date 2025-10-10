from __future__ import annotations
from collections import deque
from typing import Iterable, List
from ..domain import Cell, DragonCell
from ..strategy import KillingStrategy

class BucketsStrategy(KillingStrategy):
    """Buckets per gold value; amortized O(1) removals. O(n + G)."""
    def __init__(self, max_gold: int, last_index: int) -> None:
        self._max_g = max_gold
        self._buckets: List[deque[int]] = [deque() for _ in range(max_gold+1)]
        self._counts = [0]*(max_gold+1)
        self._sum = 0
        self._cnt = 0
        self._min_g = 1
        self._selected = [False]*(last_index+1)

    def _drop_cheapest(self) -> None:
        # Advance to next non-empty bucket.
        while self._min_g <= self._max_g and self._counts[self._min_g] == 0:
            self._min_g += 1
        if self._min_g > self._max_g:
            return
        pos = self._buckets[self._min_g].popleft()
        self._counts[self._min_g] -= 1
        self._selected[pos] = False
        self._cnt -= 1
        self._sum -= self._min_g

    def on_dragon(self, gold: int, pos: int) -> None:
        self._buckets[gold].append(pos)
        self._counts[gold] += 1
        self._selected[pos] = True
        self._cnt += 1
        self._sum += gold
        if gold < self._min_g:
            self._min_g = gold

    def enforce_before_princess(self, beauty: int) -> None:
        while self._cnt >= beauty:
            self._drop_cheapest()

    def kills_count(self) -> int: return self._cnt
    def total_gold(self) -> int: return self._sum

    def result_positions_increasing(self, cells: Iterable[Cell]) -> List[int]:
        return [c.idx for c in cells if isinstance(c, DragonCell) and self._selected[c.idx]]
