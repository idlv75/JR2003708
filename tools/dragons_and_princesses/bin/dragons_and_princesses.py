#!/usr/bin/env python3

import sys
from typing import Dict, Any
import yaml

from tools.dragons_and_princesses.core import solve_cells  # main logic


def load_yaml(path: str) -> Dict[str, Any]:
    # load YAML file into a dict
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def main() -> int:
    input_path = "tools/dragons_and_princesses/example/input.yaml"  # default path
    if len(sys.argv) >= 2:
        input_path = sys.argv[1]

    try:
        data = load_yaml(input_path)
        total, indices = solve_cells(data)
    except FileNotFoundError:
        # input file not found
        sys.stderr.write(f"Error: input file not found: {input_path}\n")
        return 2
    except yaml.YAMLError as e:
        # YAML parsing error
        sys.stderr.write(f"Error: failed to parse YAML: {e}\n")
        return 2
    except Exception as e:
        # validation or logic error
        sys.stderr.write(f"Error: {e}\n")
        return 2

    # impossible - single line "-1"
    # otherwise - total, number of dragons, indices (space separated)
    if total == -1:
        print("-1")
    else:
        print(total)
        print(len(indices))
        print(" ".join(map(str, indices)) if indices else "")

    return 0


if __name__ == "__main__":
    # entry point
    raise SystemExit(main())
