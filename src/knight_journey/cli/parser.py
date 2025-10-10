"""Parses YAML input and converts it into domain objects."""

import yaml
from typing import List, Tuple
from ..domain import Cell, DragonCell, PrincessCell

class InputParser:
    """Handles reading and validating YAML input files."""
    def __init__(self, path: str) -> None:
        self.path = path

    def parse(self) -> Tuple[List[Cell], int, int]:
        with open(self.path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        n = int(data["n"])
        cells_yaml = data["cells"]
        cells: List[Cell] = []
        max_g = 0
        for i, item in enumerate(cells_yaml, start=2):
            t = item.get("type")
            if t == "d":
                g = int(item["gold"])
                cells.append(DragonCell(idx=i, gold=g))
                if g > max_g: max_g = g
            elif t == "p":
                b = int(item["beauty"])
                cells.append(PrincessCell(idx=i, beauty=b))
            else:
                raise ValueError(f"Unknown cell type at index {i}: {t}")
        if not cells or not isinstance(cells[-1], PrincessCell):
            raise ValueError("Last cell must be a princess.")
        last = cells[-1]
        cells[-1] = PrincessCell(idx=last.idx, beauty=last.beauty, is_last=True)
        return cells, n, max_g
