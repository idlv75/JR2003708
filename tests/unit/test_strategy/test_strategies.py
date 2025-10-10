from knight_journey.strategies import HeapStrategy, BucketsStrategy
from knight_journey.domain import DragonCell, PrincessCell
from knight_journey.journey import Journey

def _cells_example():
    return [
        DragonCell(idx=2, gold=10),
        DragonCell(idx=3, gold=12),
        PrincessCell(idx=4, beauty=2),
        DragonCell(idx=5, gold=1),
        PrincessCell(idx=6, beauty=2, is_last=True),
    ], 6

def test_heap_strategy_equivalence():
    cells, n = _cells_example()
    res = Journey(cells, HeapStrategy(last_index=n)).run()
    assert res == (13, [3, 5])

def test_buckets_strategy_equivalence():
    cells, n = _cells_example()
    res = Journey(cells, BucketsStrategy(max_gold=12, last_index=n)).run()
    assert res == (13, [3, 5])
