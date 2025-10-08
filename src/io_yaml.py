

# src/io_yaml.py
import yaml
try:
    from src.models import Cell
except ModuleNotFoundError:
    from models import Cell


def _normalize_cell(it, offset):
    """Turn one YAML item into (kind:str, val:int). Supports:
       - string: "d 10" / "p 2"
       - two-item list/tuple: ["d", 10]
       - mapping: {"type": "d", "value": 10}
    """
    # string style: "d 10"
    if isinstance(it, str):
        parts = it.strip().split()
        if len(parts) != 2:
            raise ValueError(f"Cell {offset}: expected 'd 10' or 'p 2', got: {it!r}")
        return parts[0].lower(), int(parts[1])

    # two-item sequence
    if isinstance(it, (list, tuple)) and len(it) == 2:
        return str(it[0]).strip().lower(), int(it[1])

    # mapping style
    if isinstance(it, dict):
        if "type" not in it or "value" not in it:
            raise ValueError(f"Cell {offset}: each mapping needs 'type' and 'value'.")
        return str(it["type"]).strip().lower(), int(it["value"])

    raise ValueError(f"Cell {offset}: unsupported item format ({type(it).__name__}).")


def parse_yaml(path):
    """Load and validate YAML; return (n, list[Cell]) for cells 2..n."""
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict) or "n" not in data or "cells" not in data: #missing data error.
        raise ValueError("YAML must contain 'n' and 'cells'.")

    n = int(data["n"])
    items = data["cells"]

    if n < 2: # n should be at least 2.
        raise ValueError("n must be at least 2.")
    if not isinstance(items, list):
        raise ValueError("'cells' must be a list.")
    if len(items) != n - 1: # we should have at least n-1 cells excluding the first cell that doesn't have info.
        raise ValueError(f"'cells' must have exactly n-1 items; got {len(items)} for n={n}.")

    cells = []
    for offset, it in enumerate(items, start=2):
        # Accept "d 10", ["d", 10], or {"type": "d", "value": 10}
        kind, val = _normalize_cell(it, offset)
        if kind not in ("d", "p"):
            raise ValueError(f"Cell {offset}: invalid type '{kind}'. Use 'd' or 'p'.")
        if val <= 0:
            raise ValueError(f"Cell {offset}: 'value' must be positive.")
        cells.append(Cell(offset, kind, val))

    if cells[-1].kind != "p":
        raise ValueError("The last cell must be a princess (type 'p').")

    return n, cells
