from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Iterable, List
from .domain import Cell

class KillingStrategy(ABC):
    """Interface for strategies that decide which dragons to keep."""
    @abstractmethod
    def on_dragon(self, gold: int, pos: int) -> None: ...
    @abstractmethod
    def enforce_before_princess(self, beauty: int) -> None: ...
    @abstractmethod
    def kills_count(self) -> int: ...
    @abstractmethod
    def total_gold(self) -> int: ...
    @abstractmethod
    def result_positions_increasing(self, cells: Iterable[Cell]) -> List[int]: ...
