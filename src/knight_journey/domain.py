from __future__ import annotations
from abc import ABC
from dataclasses import dataclass

@dataclass(frozen=True)
class Cell(ABC):
    """Abstract base for every cell on the path."""
    idx: int

@dataclass(frozen=True)
class DragonCell(Cell):
    """A dragon cell with a certain gold value."""
    gold: int

@dataclass(frozen=True)
class PrincessCell(Cell):
    """A princess cell enforcing a kill threshold (last vs mid journey)."""
    beauty: int
    is_last: bool = False
