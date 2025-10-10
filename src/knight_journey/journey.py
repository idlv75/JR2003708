from __future__ import annotations
from typing import List, Optional, Tuple
from .domain import Cell, DragonCell, PrincessCell
from .strategy import KillingStrategy

class Journey:
    """Iterates cells left→right and delegates decisions to a strategy."""
    def __init__(self, cells: List[Cell], strategy: KillingStrategy) -> None:
        self.cells = cells
        self.strategy = strategy

    def run(self) -> Optional[Tuple[int, List[int]]]:
        """Run the journey. Returns (total, positions) or None if impossible."""
        last_beauty = None
        for c in self.cells:
            if isinstance(c, DragonCell):
                self.strategy.on_dragon(c.gold, c.idx)
            else:
                if c.is_last:
                    last_beauty = c.beauty
                else:
                    self.strategy.enforce_before_princess(c.beauty)
        if last_beauty is None or self.strategy.kills_count() < last_beauty:
            return None
        return self.strategy.total_gold(), self.strategy.result_positions_increasing(self.cells)
