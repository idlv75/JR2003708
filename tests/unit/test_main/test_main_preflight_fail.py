import sys
import textwrap
from knight_journey.__main__ import main

def test_main_preflight_fail(capsys, tmp_path):
    yml = tmp_path / "input.yaml"
    yml.write_text(textwrap.dedent("""
        n: 4
        cells:
          - {type: p, beauty: 1}
          - {type: p, beauty: 5}
          - {type: p, beauty: 1}
    """).strip() + "\n", encoding="utf-8")
    argv_backup = sys.argv[:]
    try:
        sys.argv = ["prog", "--input", str(yml)]
        main()
    finally:
        sys.argv = argv_backup
    out = capsys.readouterr().out.strip()
    assert "-1" in out
