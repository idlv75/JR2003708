from typing import Union, List

import sys
import yaml


class Dragon:
    def __init__(self, index, gold):
        self.index = index
        self.gold = gold

class Princess:
    def __init__(self, index, beauty):
        self.index = index
        self.beauty = beauty

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
        try:
            cell_type, value = entry.split()
            value = int(value)
        except Exception:
            raise ValueError(f"Invalid cell format at line {i}: expected 'd/p number'")

        if cell_type == "d":
            cells.append(Dragon(index=i, gold=value))
        elif cell_type == "p":
            cells.append(Princess(index=i, beauty=value))
        else:
            raise ValueError(f"Unknown cell type '{cell_type}' at line {i}")

    if len(cells) != number_of_cells - 1:
        raise ValueError("Invalid input: number of cells does not match the given n")
    if not isinstance(cells[-1], Princess):
        raise ValueError("Invalid input: last cell must be a princess!")

    return cells

def main():
    if len(sys.argv) < 2:
        print("Error: missing input file.\nUse files: dragons_and_princesses.py, input.yaml")
        sys.exit(1)

    yaml_file = sys.argv[1]
    try:
        cells = load_journey_map(yaml_file)
        print("map loaded")
        for c in cells:
            if isinstance(c, Dragon):
                print(f"Dragon cell: {c.index}, gold: {c.gold}")
            else:
                print(f"Princess cell: {c.index}, beauty: {c.beauty}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)




if __name__ == "__main__":
    main()
