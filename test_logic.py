import pytest
from src.logic import Dragon, Princess, get_journey_result


def test_not_killed_enough_dragons():
    cells = [
        Dragon(2, 5),
        Princess(3, 1),
        Dragon(4, 10),
        Princess(5, 2),
    ]
    gold, killed = get_journey_result(cells)
    assert gold == -1


def test_reached_last_princess():
    cells = [
        Dragon(2, 5),
        Princess(3, 3),
        Dragon(4, 10),
        Princess(5, 2),
    ]
    gold, killed = get_journey_result(cells)
    assert gold == 15
    assert killed == [2, 4]


def test_no_dragons():
    cells = [
        Princess(2, 1),
        Princess(3, 2),
    ]
    gold, killed = get_journey_result(cells)
    assert gold == -1


def test_exact_beauty_match():
    cells = [
        Dragon(2, 10),
        Dragon(3, 20),
        Princess(4, 2),
    ]
    gold, killed = get_journey_result(cells)
    assert gold == 30
    assert killed == [2, 3]


def test_unreachable_final_princess():
    cells = [
        Dragon(2, 10),
        Dragon(3, 12),
        Princess(4, 2),
        Dragon(5, 1),
        Princess(6, 3),
    ]
    gold, killed = get_journey_result(cells)
    assert gold == -1


def test_no_princess_at_end():
    cells = [
        Dragon(2, 5),
        Princess(3, 2),
        Dragon(4, 10),  # ends with dragon
    ]
    with pytest.raises(ValueError):
        get_journey_result(cells)
