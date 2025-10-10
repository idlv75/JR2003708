from knight_journey.cli.strategy_selector import StrategySelector
from knight_journey.strategies import HeapStrategy, BucketsStrategy

def test_selector_prefers_buckets_for_small_G_large_n():
    sel = StrategySelector(n=200_000, max_gold=10_000)
    s = sel.choose()
    assert isinstance(s, BucketsStrategy)

def test_selector_prefers_heap_when_G_is_huge_and_n_small():
    sel = StrategySelector(n=1_000, max_gold=10_000_000)
    s = sel.choose()
    assert isinstance(s, HeapStrategy)
