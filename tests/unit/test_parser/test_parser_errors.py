import textwrap
import pytest
from knight_journey.cli.parser import InputParser

def test_parser_invalid_type_raises(tmp_path):
    yml = tmp_path / "bad.yaml"
    yml.write_text(textwrap.dedent("""
        n: 3
        cells:
          - {type: x, gold: 10}
          - {type: p, beauty: 1}
    """).strip() + "\n", encoding="utf-8")
    p = InputParser(str(yml))
    with pytest.raises(ValueError):
        p.parse()
