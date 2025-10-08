#!/usr/bin/env python3
"""
Dragons and Princesses Problem Solution
CodeForces Problem #548

This module provides a solution for the Dragons and Princesses problem
using a greedy algorithm with Union-Find data structure.
"""

import sys
from typing import List, Tuple, Optional
from dataclasses import dataclass

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


@dataclass(frozen=True)
class Cell:
    """Immutable representation of a cell in the game."""
    cell_type: str  # 'd' for dragon, 'p' for princess
    value: int      # gold for dragon, beauty requirement for princess
    position: int   # position in the game


class DragonsAndPrincessesSolver:
    """Solver for the Dragons and Princesses problem using greedy algorithm."""
    
    def __init__(self, cells: List[Cell]):
        """Initialize solver with game cells."""
        self.cells = cells
        self.n = len(cells) + 1  # +1 because cells are 2..n
    
    def solve(self) -> Optional[Tuple[int, List[int]]]:
        """
        Solve the Dragons and Princesses problem.
        
        Returns:
            Tuple of (total_gold, killed_dragon_positions) or None if no solution
        """
        if not self.cells:
            return None
            
        # Extract princess positions
        princess_positions = []
        for cell in self.cells:
            if cell.cell_type == 'p':
                princess_positions.append((cell.position, cell.value))
        
        m = len(princess_positions)
        if m == 0:
            return None
            
        # Record beauties
        beauties = [b for (_, b) in princess_positions]
        
        # Assign dragons to segments
        tasks_early = []  # (gold, position, segment index)
        tasks_final = []  # (gold, position)
        seg_idx = 1
        p_ptr = 0
        
        for cell in self.cells:
            if cell.cell_type == 'p':
                seg_idx += 1
                p_ptr += 1
                continue
            # Dragon
            g = cell.value
            if seg_idx < m:
                tasks_early.append((g, cell.position, seg_idx))
            else:
                tasks_final.append((g, cell.position))
        
        # Compute capacities c_j for j=1..m-1
        c = [0] * m
        if m > 1:
            temp = [0] * (m - 1)
            temp[m - 2] = max(0, beauties[m - 2] - 1)
            for j in range(m - 3, -1, -1):
                v = max(0, beauties[j] - 1)
                temp[j] = min(v, temp[j + 1])
            for j in range(m - 1):
                c[j] = temp[j]
        
        # Feasibility check
        max_cap = c[m - 2] if m > 1 else 0
        total_final = len(tasks_final)
        if max_cap + total_final < beauties[m - 1]:
            return None
        
        # Greedy selection of early dragons using Union-Find
        selected_early = []
        gold_early = 0
        if max_cap > 0 and tasks_early:
            tasks_early.sort(key=lambda x: (-x[0], x[1]))
            parent = list(range(max_cap + 1))
            
            def find(x):
                while parent[x] != x:
                    parent[x] = parent[parent[x]]
                    x = parent[x]
                return x
            
            for g, pos, seg in tasks_early:
                d_cap = c[seg - 1]
                if d_cap <= 0:
                    continue
                slot = find(d_cap)
                if slot == 0:
                    continue
                parent[slot] = slot - 1
                selected_early.append(pos)
                gold_early += g
        
        # Always include all final-segment dragons
        selected_final = [pos for (g, pos) in tasks_final]
        gold_final = sum(g for (g, pos) in tasks_final)
        
        kills = len(selected_early) + len(selected_final)
        if kills < beauties[m - 1]:
            return None
        
        total_gold = gold_early + gold_final
        result_positions = selected_early + selected_final
        result_positions.sort()
        
        return total_gold, result_positions


def read_yaml_input(file_path: str) -> List[Cell]:
    """Read input from YAML file."""
    if not YAML_AVAILABLE:
        raise ImportError("PyYAML is required to read YAML files. Install it with: pip install PyYAML")
    
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
    
    cells = []
    for cell_data in data['cells']:
        cell = Cell(
            cell_type=cell_data['type'],
            value=cell_data['value'],
            position=cell_data['position']
        )
        cells.append(cell)
    
    return cells


def read_stdin_input() -> List[Cell]:
    """Read input from standard input."""
    input_data = sys.stdin.read().strip().splitlines()
    n = int(input_data[0])
    
    cells = []
    for idx, line in enumerate(input_data[1:], start=2):
        cell_type, value = line.split()
        value = int(value)
        cell = Cell(cell_type=cell_type, value=value, position=idx)
        cells.append(cell)
    
    return cells


def main():
    """Main function to solve the Dragons and Princesses problem."""
    if len(sys.argv) > 1:
        # Read from YAML file
        cells = read_yaml_input(sys.argv[1])
    else:
        # Read from stdin
        cells = read_stdin_input()
    
    solver = DragonsAndPrincessesSolver(cells)
    result = solver.solve()
    
    if result is None:
        print(-1)
    else:
        total_gold, killed_dragons = result
        print(total_gold)
        print(len(killed_dragons))
        if killed_dragons:
            print(" ".join(map(str, killed_dragons)))


if __name__ == '__main__':
    main()
