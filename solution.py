"""
Solution for the 'Dragons and Princesses' problem.

Author: Tzipora Shenker
Description:
    Given a sequence of cells, each containing either a dragon with gold 
    or a princess with beauty value, this program determines the maximum
    amount of gold that can be collected while satisfying the rules of
    killing dragons before meeting each princess.
"""

import yaml
from dataclasses import dataclass
from typing import List, Tuple, Optional
from heapq import heappush, heappop

@dataclass(frozen=True)
class Cell:
    """
    Represents a single cell in the journey.

    Attributes:
        type (str): 'd' for dragon, 'p' for princess.
        value (int): The gold of a dragon or the beauty requirement of a princess.
    """
    type: str   
    value: int

def max_gold_with_dragons(n: int, cells: List[Cell]) -> Optional[Tuple[int, List[int]]]:
    """
    Calculates the maximum gold obtainable based on the given sequence of cells.

    Args:
        n (int): The number of cells in the path.
        cells (List[Cell]): List of Cell objects representing dragons or princesses.

    Returns:
        Optional[Tuple[int, List[int]]]:
            A tuple of (total gold collected, list of dragon indices) 
            if the journey is possible, or None if it is not.
    """
    total_gold = 0
    dragons_killed: List[int] = []
    killed_count = 0
    current_heap: List[Tuple[int, int]] = []

    last_idx = n - 2  # index of the last princess in the cells list

    for idx, cell in enumerate(cells, start=2):
        if cell.type == 'd':
            heappush(current_heap, (-cell.value, idx))
        else:  # princess
            beauty = cell.value
            if idx-2 != last_idx:  # intermediate princess
                max_kill = beauty - 1
                while current_heap and killed_count < max_kill:
                    g_neg, cell_number = heappop(current_heap)
                    total_gold += -g_neg
                    dragons_killed.append(cell_number)
                    killed_count += 1
                current_heap.clear()
            else:  # last princess
                while killed_count < beauty:
                    if not current_heap:
                        return None
                    g_neg, cell_number = heappop(current_heap)
                    total_gold += -g_neg
                    dragons_killed.append(cell_number)
                    killed_count += 1
                while current_heap:
                    g_neg, cell_number = heappop(current_heap)
                    total_gold += -g_neg
                    dragons_killed.append(cell_number)
    return total_gold, sorted(dragons_killed)

def read_input_yaml(file_path: str) -> Tuple[int, List[Cell]]:
    """
    Reads the input YAML file and converts its contents into Cell objects.

    Args:
        file_path (str): Path to the YAML input file.

    Returns:
        Tuple[int, List[Cell]]: The total number of cells and the corresponding list.
    """
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
    cells = [Cell(**c) for c in data['cells']]
    return data['n'], cells


def main():
    """
    Main entry point of the program.
    Reads input, executes the algorithm, and prints the results.
    """
    n, cells = read_input_yaml('input.yaml')
    result = max_gold_with_dragons(n, cells)
    if result is None:
        print(-1)
    else:
        total_gold, dragons = result
        print(total_gold)
        print(len(dragons))
        print(' '.join(map(str, dragons)))


if __name__ == '__main__':
    main()
