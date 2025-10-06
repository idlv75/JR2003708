#!/usr/bin/env python3
"""
Dragons and Princesses Solution
Files:
dragons_and_princesses.py,test_dragons_and_princesses.py input.yaml
"""

import heapq
from dataclasses import dataclass
from typing import Union, List, Tuple
import sys
import yaml

@dataclass(frozen=True) # cannot be changed once created
class Dragon:
    index: int
    gold: int

@dataclass(frozen=True)
class Princess:
    index: int
    beauty: int

# union type to represent either a Dragon or a Princess cell
Cell = Union[Dragon, Princess]


def load_journey_map(filepath: str) -> List[Cell]:
    """
    Loads the knight’s journey map from a YAML file
    and builds a list of game cells (dragons and princesses)
    """
    with open(filepath, "r") as f:
        data = yaml.safe_load(f)

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


def get_journey_result(cells: List[Cell]) -> Tuple[int, List[int]]:
    """
    Checks whether the knight can reach the final princess
    and if so, returns the maximum amount of gold he can
    collect in the way and the indices of the dragons he killed
    """
    heap = [] # keeps dragons gold in a min heap
    total_gold = 0

    for cell in cells[:-1]: # skip last cell (final princess)
        if isinstance(cell, Dragon):
            # collect gold and add dragon to heap
            heapq.heappush(heap, (cell.gold, cell.index))
            total_gold += cell.gold
        elif isinstance(cell, Princess):
            # if too many dragons were killed, remove the ones that has the fewest gold
            while len(heap) >= cell.beauty:
                gold, _ = heapq.heappop(heap)
                total_gold -= gold

    last_princess = cells[-1]
    try:
        if not isinstance(last_princess, Princess):
            raise ValueError("Last cell must be a princess!")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    # if the knight hasnt killed enough dragons he cant marry last princess
    if len(heap) < last_princess.beauty:
        return -1, []

    # otherwise return total gold and list of killed dragon indices
    killed_dragons_pos = sorted(idx for _, idx in heap)
    return total_gold, killed_dragons_pos


def main():
    if len(sys.argv) < 2:
        print("Error: missing input file.\nUse files: dragons_and_princesses.py, input.yaml")
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
