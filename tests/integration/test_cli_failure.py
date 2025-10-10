import sys, subprocess, textwrap

def test_cli_failure_impossible_last_princess(tmp_path):
    yaml_path = tmp_path / "input.yaml"
    yaml_path.write_text(
        textwrap.dedent("""\n        n: 6\n        cells:\n          - type: d\n            gold: 2\n          - type: p\n            beauty: 1\n          - type: d\n            gold: 3\n          - type: p\n            beauty: 5\n        """).strip() + "\n",
        encoding="utf-8"
    )
    proc = subprocess.run(
        [sys.executable, "-m", "knight_journey", "--input", str(yaml_path)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False
    )
    assert "-1" in proc.stdout.strip().splitlines()
