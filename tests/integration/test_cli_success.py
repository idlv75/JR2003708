import sys, subprocess, textwrap

def test_cli_success(tmp_path):
    yaml_path = tmp_path / "input.yaml"
    yaml_path.write_text(
        textwrap.dedent("""\n        n: 6\n        cells:\n          - type: d\n            gold: 10\n          - type: d\n            gold: 12\n          - type: p\n            beauty: 2\n          - type: d\n            gold: 1\n          - type: p\n            beauty: 2\n        """).strip() + "\n",
        encoding="utf-8"
    )
    proc = subprocess.run(
        [sys.executable, "-m", "knight_journey", "--input", str(yaml_path)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False
    )
    assert proc.returncode == 0
    lines = proc.stdout.strip().splitlines()
    assert lines[0] == "13"
    assert lines[1] == "2"
    assert lines[2].strip() == "3 5"
