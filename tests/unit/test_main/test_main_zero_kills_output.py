import sys
import textwrap
from knight_journey.__main__ import main

def test_main_zero_kills_format(capsys, tmp_path):
    # Last princess beauty=0 → no final constraint → keep the dragon for max gold
    yml = tmp_path / "input.yaml"
    yml.write_text(textwrap.dedent("""
        n: 4
        cells:
          - {type: p, beauty: 100}
          - {type: d, gold: 5}
          - {type: p, beauty: 0}
    """).strip() + "\n", encoding="utf-8")

    argv_backup = sys.argv[:]
    try:
        sys.argv = ["prog", "--input", str(yml)]
        main()
    finally:
        sys.argv = argv_backup

    lines = capsys.readouterr().out.splitlines()
    assert int(lines[0]) == 5      # total gold
    assert lines[1].strip() == "1" # kills count
    assert lines[2].strip() == "3" # positions list
