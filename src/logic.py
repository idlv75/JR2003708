"""
Core logic for the Dragons and Princesses problem

Implements the main algorithm for determining whether the knight
can reach the final princess and if so calculates the
maximum total gold collected and the indices of the killed dragons

Complexity: O(nlogn)
"""

import heapq
from dataclasses import dataclass
from typing import Union, List, Tuple


@dataclass(frozen=True)  # cannot be changed once created
class Dragon:
    index: int
    gold: int


@dataclass(frozen=True)
class Princess:
    index: int
    beauty: int


# union type to represent either a Dragon or a Princess cell
Cell = Union[Dragon, Princess]


def get_journey_result(cells: List[Cell]) -> Tuple[int, List[int]]:
    """
    Checks whether the knight can reach the final princess
    and if so, returns the maximum amount of gold he can
    collect in the way and the indices of the dragons he killed
    """
    heap = []  # keeps dragons gold in a min heap
    total_gold = 0

    for cell in cells[:-1]:  # skip last cell (final princess)
        if isinstance(cell, Dragon):
            # collect gold and add dragon to heap
            heapq.heappush(heap, (cell.gold, cell.index))
            total_gold += cell.gold
        elif isinstance(cell, Princess):
            # if too many dragons were killed, remove the ones that has the fewest gold
            while len(heap) >= cell.beauty:
                gold, _ = heapq.heappop(heap)
                total_gold -= gold

    last_princess = cells[-1]
    if not isinstance(last_princess, Princess):
        raise ValueError("Invalid input: last cell must be a princess!")

    # if the knight hasn't killed enough dragons he can't marry last princess
    if len(heap) < last_princess.beauty:
        return -1, []

    # otherwise return total gold and list of killed dragon indices
    killed_dragons_pos = sorted(idx for _, idx in heap)
    return total_gold, killed_dragons_pos
