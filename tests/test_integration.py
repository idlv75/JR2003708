import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.io_yaml import parse_yaml
from src.planner import compute_plan

def test_example_yaml_roundtrip():
    ypath = os.path.join(os.path.dirname(__file__), "data", "ex_ok.yaml")
    n, cells = parse_yaml(ypath)
    total, idxs = compute_plan(n, cells)
    assert total == 13
    assert idxs == [3, 5]
