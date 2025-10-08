import os, sys, subprocess
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.io_yaml import parse_yaml
from src.planner import compute_plan
import pytest

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# filename -> expected
# ("ok", total, indices) or ("imp",)
CASES = {
    "ex_ok.yaml": ("ok", 13, [3, 5]),
    "ex_impossible.yaml": ("imp",),
    "ex_many_princesses.yaml": ("ok", 14, [4, 6]),
    "ex_all_dragons_ok.yaml": ("ok", 12, [2, 3, 4]),   # was 10,[2,3]
    "ex_early_strict.yaml": ("ok", 9, [5]),            # was ("imp",)
}


@pytest.mark.parametrize("fname", sorted(CASES.keys()))
def test_planner_against_fixtures(fname):
    kind = CASES[fname][0]
    n, cells = parse_yaml(os.path.join(DATA_DIR, fname))

    if kind == "ok":
        _, total_exp, idxs_exp = CASES[fname]
        total, idxs = compute_plan(n, cells)
        assert total == total_exp
        assert idxs == idxs_exp
    else:
        with pytest.raises(ValueError) as e:
            compute_plan(n, cells)
        assert str(e.value) == "IMPOSSIBLE"

@pytest.mark.parametrize("fname", sorted(CASES.keys()))
def test_cli_against_fixtures(fname):
    kind = CASES[fname][0]
    ypath = os.path.join(DATA_DIR, fname)

    # Run from the REPO ROOT and call the module entrypoint:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    cmd = [sys.executable, "-m", "src.solver", ypath]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=repo_root)

    out = proc.stdout.strip().splitlines()

    if kind == "imp":
        assert out == ["-1"], f"stderr: {proc.stderr}"
    else:
        _, total_exp, idxs_exp = CASES[fname]
        assert len(out) >= 2, f"no output. stderr: {proc.stderr}"
        total = int(out[0])
        k = int(out[1])
        indices = []
        if len(out) >= 3 and out[2].strip():
            indices = list(map(int, out[2].split()))
        assert total == total_exp
        assert indices == idxs_exp
        assert k == len(idxs_exp)

