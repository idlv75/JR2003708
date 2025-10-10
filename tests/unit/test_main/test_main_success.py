import sys
import textwrap
from knight_journey.__main__ import main

def test_main_success(capsys, tmp_path):
    yml = tmp_path / "input.yaml"
    yml.write_text(textwrap.dedent("""
        n: 6
        cells:
          - {type: d, gold: 10}
          - {type: d, gold: 12}
          - {type: p, beauty: 2}
          - {type: d, gold: 1}
          - {type: p, beauty: 2}
    """).strip() + "\n", encoding="utf-8")
    argv_backup = sys.argv[:]
    try:
        sys.argv = ["prog", "--input", str(yml)]
        main()
    finally:
        sys.argv = argv_backup
    out = capsys.readouterr().out.strip().splitlines()
    assert out[0] == "13"
    assert out[1] == "2"
    assert out[2] == "3 5"
