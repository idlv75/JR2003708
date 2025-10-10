from knight_journey.cli.parser import InputParser
from knight_journey.domain import PrincessCell

def test_parser_marks_last_princess(tmp_path):
    p = tmp_path / "input.yaml"
    p.write_text(
        "n: 5\n"
        "cells:\n"
        "  - {type: d, gold: 3}\n"
        "  - {type: p, beauty: 1}\n"
        "  - {type: p, beauty: 1}\n"
        "  - {type: p, beauty: 2}\n", encoding="utf-8"
    )
    cells, n, max_g = InputParser(str(p)).parse()
    assert n == 5
    assert max_g == 3
    assert isinstance(cells[-1], PrincessCell) and cells[-1].is_last
