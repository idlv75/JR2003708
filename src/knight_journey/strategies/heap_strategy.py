from __future__ import annotations
import heapq
from typing import Iterable, List, Tuple
from ..domain import Cell, DragonCell
from ..strategy import KillingStrategy

class HeapStrategy(KillingStrategy):
    """Min-heap; always drops the cheapest dragon first. O(n log n)."""
    def __init__(self, last_index: int) -> None:
        self._heap: List[Tuple[int,int]] = []    # (gold, pos)
        self._sum = 0
        self._selected = [False]*(last_index+1)  # bitmap by board index

    def on_dragon(self, gold: int, pos: int) -> None:
        heapq.heappush(self._heap, (gold, pos))
        self._sum += gold
        self._selected[pos] = True

    def enforce_before_princess(self, beauty: int) -> None:
        # Keep invariant: kills < beauty
        while len(self._heap) >= beauty:
            g, p = heapq.heappop(self._heap)
            self._sum -= g
            self._selected[p] = False

    def kills_count(self) -> int: return len(self._heap)
    def total_gold(self) -> int: return self._sum

    def result_positions_increasing(self, cells: Iterable[Cell]) -> List[int]:
        # Scan in input order to avoid sorting.
        return [c.idx for c in cells if isinstance(c, DragonCell) and self._selected[c.idx]]
