import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.models import Cell
from src.planner import compute_plan
import pytest

def test_happy_path():
    n = 6
    cells = [
        Cell(2, "d", 10),
        Cell(3, "d", 12),
        Cell(4, "p", 2),
        Cell(5, "d", 1),
        Cell(6, "p", 2),
    ]
    total, idxs = compute_plan(n, cells)
    assert total == 13
    assert idxs == [3, 5]

def test_impossible_final():
    n = 6
    cells = [
        Cell(2, "d", 10),
        Cell(3, "d", 12),
        Cell(4, "p", 2),
        Cell(5, "d", 1),
        Cell(6, "p", 3),
    ]
    with pytest.raises(ValueError) as e:
        compute_plan(n, cells)
    assert str(e.value) == "IMPOSSIBLE"

def test_multiple_princesses_keep_max_gold():
    n = 7
    cells = [
        Cell(2, "d", 5),
        Cell(3, "p", 1),
        Cell(4, "d", 4),
        Cell(5, "p", 2),
        Cell(6, "d", 10),
        Cell(7, "p", 2),
    ]
    total, idxs = compute_plan(n, cells)
    assert total == 14
    assert idxs == [4, 6]
