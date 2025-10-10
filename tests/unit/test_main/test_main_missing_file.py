import sys
from knight_journey.__main__ import main

def test_main_missing_file_prints_minus_one(capsys, tmp_path):
    missing = tmp_path / "no_such_input.yaml"
    argv_backup = sys.argv[:]
    try:
        sys.argv = ["prog", "--input", str(missing)]
        main()
    finally:
        sys.argv = argv_backup
    out = capsys.readouterr().out.strip()
    assert "-1" in out
