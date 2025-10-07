#!/usr/bin/env python3
"""
Main script for Dragons and Princesses Solution
Reads the knight's journey map from a YAML file,
invokes the solver and prints the results
"""

import sys
from typing import List
import yaml
from pathlib import Path
from logic import Dragon, Princess, Cell, get_journey_result


def load_journey_map(filepath: str) -> List[Cell]:
    """
    Loads the knight's journey map from a YAML file
    and builds a list of game cells (dragons and princesses).
    Each cell in the returned list is represented as either
    a Dragon or a Princess object.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(path, "r") as f:
        data = yaml.safe_load(f)
    # validate YAML structure
    try:
        number_of_cells = data["n"]
        raw_cells = data["cells"]
    except Exception:
        raise ValueError("Invalid input format: expected 'n' and 'cells' fields in yaml file")

    cells = []
    for i, entry in enumerate(raw_cells, start=2):
        # make sure the yaml file has the required fields
        try:
            cell_type, value = entry.split()
            value = int(value)
        except Exception:
            raise ValueError(f"Invalid cell format at line {i}: expected 'd/p number'")
        # build objects based on cell type
        if cell_type == "d":
            cells.append(Dragon(index=i, gold=value))
        elif cell_type == "p":
            cells.append(Princess(index=i, beauty=value))
        else:
            raise ValueError(f"Unknown cell type '{cell_type}' at line {i}")
    # validate the total number of cells and ensure last one is a princess
    if len(cells) != number_of_cells - 1:
        raise ValueError("Invalid input: number of cells does not match the given n")
    if not isinstance(cells[-1], Princess):
        raise ValueError("Invalid input: last cell must be a princess!")

    return cells


def main():
    """
    Entry point of the program.
    Reads the input YAML file, computes the knight's journey result
    and prints the output according to the problem format.
    """
    if len(sys.argv) < 2:
        print("Error: missing input file.\nUse files: ./src/main.py input.yaml")
        sys.exit(1)

    yaml_file = sys.argv[1]
    try:
        cells = load_journey_map(yaml_file)
        total_gold, killed_dragons_pos = get_journey_result(cells)
        # handle no solution case
        if total_gold == -1:
            print(-1)
        else:
            # print result: total gold, count and dragon indices
            print(total_gold)
            print(len(killed_dragons_pos))
            if killed_dragons_pos:
                print(*killed_dragons_pos)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
