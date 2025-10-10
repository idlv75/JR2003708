from knight_journey.journey import Journey
from knight_journey.domain import DragonCell, PrincessCell
from knight_journey.strategies import BucketsStrategy

def test_journey_returns_none_when_final_condition_unsatisfied():
    cells = [
        DragonCell(idx=2, gold=10),
        DragonCell(idx=3, gold=12),
        PrincessCell(idx=4, beauty=2),
        DragonCell(idx=5, gold=1),
        PrincessCell(idx=6, beauty=3, is_last=True),
    ]
    res = Journey(cells, BucketsStrategy(max_gold=12, last_index=6)).run()
    assert res is None
