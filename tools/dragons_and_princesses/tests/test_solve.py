import pytest
from typing import List, Dict, Any
from tools.dragons_and_princesses.core import solve_cells


# Parametrized tests for multiple scenarios
@pytest.mark.parametrize(
    "n, cells, expected_total, expected_indices",
    [
        pytest.param(
            # Basic sample – should return 13 and 3 5
            6,
            [
                {"type": "start"},
                {"type": "d", "g": 10},
                {"type": "d", "g": 12},
                {"type": "p", "b": 2},
                {"type": "d", "g": 1},
                {"type": "p", "b": 2},
            ],
            13,
            [3, 5],
            id="sample1_total_13_indices_3_5",
        ),
        pytest.param(
            # Impossible at final princess – should return -1
            6,
            [
                {"type": "start"},
                {"type": "d", "g": 10},
                {"type": "d", "g": 12},
                {"type": "p", "b": 2},
                {"type": "d", "g": 1},
                {"type": "p", "b": 3},   # final needs >= 3 (we have only 2)
            ],
            -1,
            [],
            id="sample2_impossible_minus_one",
        ),
        pytest.param(
            # Final princess at the end (n=3) – needs >=1, we have 1
            3,
            [
                {"type": "start"},
                {"type": "d", "g": 11},
                {"type": "p", "b": 1},
            ],
            11,
            [2],
            id="final_at_end_p1_total_11",
        ),
    ],
)
def test_scenarios(
    n: int, cells: List[Dict[str, Any]], expected_total: int, expected_indices: List[int]
) -> None:
    data = {"n": n, "cells": cells}
    total, indices = solve_cells(data)
    assert total == expected_total
    assert indices == expected_indices  # indices must be ascending


# Validation - missing/invalid fields and ranges
def test_invalid_missing_n() -> None:
    data = {
        # missing n
        "cells": [
            {"type": "start"},
            {"type": "p", "b": 1}
        ]
    }
    with pytest.raises(ValueError):
        solve_cells(data)


def test_invalid_n_not_int() -> None:
    data = {
        "n": "6",  # not int
        "cells": [
            {"type": "start"},
            {"type": "p", "b": 1}
        ]
    }
    with pytest.raises(ValueError):
        solve_cells(data)


def test_invalid_cells_not_list() -> None:
    data = {
        "n": 2,
        "cells": "not-a-list"  # not list
    }
    with pytest.raises(ValueError):
        solve_cells(data)


def test_invalid_len_cells() -> None:
    data = {
        "n": 4,
        "cells": [
            {"type": "start"},
            {"type": "p", "b": 1}
        ]
    }
    with pytest.raises(ValueError):
        solve_cells(data)


def test_invalid_last_not_princess() -> None:
    data = {
        "n": 3,
        "cells": [
            {"type": "start"},
            {"type": "d", "g": 5},
            {"type": "d", "g": 7}  # not princess
        ]
    }
    with pytest.raises(ValueError):
        solve_cells(data)


def test_invalid_unknown_event_type() -> None:
    data = {
        "n": 3,
        "cells": [
            {"type": "start"},
            {"type": "troll", "g": 9},  # invalid type
            {"type": "p", "b": 1}
        ]
    }
    with pytest.raises(ValueError):
        solve_cells(data)


def test_invalid_non_integer_gold() -> None:
    data = {
        "n": 2,
        "cells": [
            {"type": "start"},
            {"type": "d", "g": 3.5}  # not int
        ]
    }
    with pytest.raises(ValueError):
        solve_cells(data)


def test_invalid_non_integer_beauty() -> None:
    data = {
        "n": 2,
        "cells": [
            {"type": "start"},
            {"type": "p", "b": "2"}  # not int
        ]
    }
    with pytest.raises(ValueError):
        solve_cells(data)


@pytest.mark.parametrize("bad_b", [0, 200001])
def test_invalid_beauty_out_of_range(bad_b: int) -> None:
    data = {
        "n": 2,
        "cells": [
            {"type": "start"},
            {"type": "p", "b": bad_b}  # out of [1..200000]
        ]
    }
    with pytest.raises(ValueError):
        solve_cells(data)


@pytest.mark.parametrize("bad_g", [0, 10001])
def test_invalid_gold_out_of_range(bad_g: int) -> None:
    data = {
        "n": 2,
        "cells": [
            {"type": "start"},
            {"type": "d", "g": bad_g}  # out of [1..10000]
        ]
    }
    with pytest.raises(ValueError):
        solve_cells(data)


@pytest.mark.parametrize("bad_n", [1, 200001])
def test_invalid_n_out_of_range(bad_n: int) -> None:
    data = {
        "n": bad_n,  # out of [2..200000]
        "cells": [
            {"type": "start"},
            {"type": "p", "b": 1}
        ]
    }
    with pytest.raises(ValueError):
        solve_cells(data)
