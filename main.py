# Implement reading from a YAML file
# Implement a solution in python for the #548 CodeForces problem.
import sys
import yaml
from pathlib import Path

def load_data():    
    if len(sys.argv) > 1:
        data_path = sys.argv[1]
    else:
        data_path = "example_data.yaml"

    path = Path(data_path)

    if not path.exists():
        print("File not found:", data_path)
        sys.exit(1)

    with open(path, "r") as file:
        try:
            data = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)

    n = data["n"]
    cells = []
    for cell in data["cells"]:
        cell_type, val = cell.split()
        cells.append((cell_type, int(val)))
    return n, cells

def main():
    n, cells = load_data()
    kills = 0
    dragons_killed = []
    total_gold = 0
    desired_princess_beauty = cells[-1][1]

    for index,(cell_type, val) in enumerate(cells, start=2):
        if cell_type == 'd':
            dragons_killed.append((index, val))
            kills += 1
            total_gold += val
        else:
            while index < n and kills >= val and dragons_killed:
                weakest = min(dragons_killed, key=lambda dragon: dragon[1]) # dragon[1] = value / Gold.
                dragons_killed.remove(weakest)
                total_gold -= weakest[1]
                kills -= 1

    if kills >= desired_princess_beauty:
        print(total_gold)
        print(len(dragons_killed))
        for dragon in dragons_killed:
            print(dragon[0], end = ' ')
        print() # To add a new line after the dragon indexes were printed
        return 1 # For Unittesting purposes only
    else:
        print("-1")
        return 0 # For Unittesting purposes only

if __name__ == "__main__": # This matters for execution / imports 
    main()