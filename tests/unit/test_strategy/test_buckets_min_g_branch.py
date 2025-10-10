from knight_journey.strategies import BucketsStrategy

def test_buckets_min_g_resets_when_new_smaller_gold_arrives():
    s = BucketsStrategy(max_gold=10, last_index=20)
    s._drop_cheapest()
    old_min = s._min_g
    assert old_min > s._max_g
    s.on_dragon(7, 3)
    assert s._min_g == 7
