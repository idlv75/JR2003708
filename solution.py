#!/usr/bin/env python3

from dataclasses import dataclass
from typing import Tuple, Optional
from itertools import combinations
import yaml
import sys


@dataclass(frozen=True)
class Dragon:
    position: int
    gold: int


@dataclass(frozen=True)
class Princess:
    position: int
    beauty: int


@dataclass(frozen=True)
class Cell:
    position: int
    cell_type: str
    value: int


def parse_yaml(data):
    number_of_cells = data['n']
    cells = tuple(
        Cell(position=index + 2, cell_type=cell['type'], value=cell['value'])
        for index, cell in enumerate(data['cells'])
    )
    return number_of_cells, cells


def split_entities(cells):
    dragons = tuple(
        Dragon(position=cell.position, gold=cell.value) 
        for cell in cells if cell.cell_type == 'd'
    )
    princesses = tuple(
        Princess(position=cell.position, beauty=cell.value) 
        for cell in cells if cell.cell_type == 'p'
    )
    return dragons, princesses


def is_valid_selection(dragons, princesses, selected_indices):
    for princess in princesses:
        kills_before = sum(
            1 for dragon_index in selected_indices 
            if dragons[dragon_index].position < princess.position
        )
        if kills_before >= princess.beauty:
            return False
    return True


def find_best_dragons(dragons, intermediate_princesses, dragons_needed):
    dragon_indices = list(range(len(dragons)))
    dragon_indices.sort(key=lambda index: dragons[index].gold, reverse=True)
    
    greedy_selection = set(dragon_indices[:dragons_needed])
    if is_valid_selection(dragons, intermediate_princesses, greedy_selection):
        return tuple(sorted(greedy_selection))
    
    best_gold_amount = -1
    best_combination = None
    
    for combination in combinations(range(len(dragons)), dragons_needed):
        if is_valid_selection(dragons, intermediate_princesses, set(combination)):
            total_gold = sum(dragons[index].gold for index in combination)
            if total_gold > best_gold_amount:
                best_gold_amount = total_gold
                best_combination = combination
    
    return tuple(sorted(best_combination)) if best_combination else None


def solve_problem(number_of_cells, cells):
    dragons, princesses = split_entities(cells)
    
    if not princesses:
        return -1, ()
    
    target_princess = princesses[-1]
    intermediate_princesses = princesses[:-1]
    dragons_needed = target_princess.beauty
    
    if dragons_needed > len(dragons):
        return -1, ()
    
    selected_dragon_indices = find_best_dragons(dragons, intermediate_princesses, dragons_needed)
    
    if selected_dragon_indices is None:
        return -1, ()
    
    total_gold = sum(dragons[index].gold for index in selected_dragon_indices)
    dragon_positions = tuple(dragons[index].position for index in selected_dragon_indices)
    
    return total_gold, dragon_positions


def format_result(total_gold, dragon_positions):
    if total_gold == -1:
        return "-1"
    
    result_lines = [str(total_gold), str(len(dragon_positions))]
    if dragon_positions:
        result_lines.append(" ".join(map(str, dragon_positions)))
    
    return "\n".join(result_lines)


def main():
    if len(sys.argv) != 2:
        print("Usage: python solution.py <input.yaml>")
        sys.exit(1)
    
    with open(sys.argv[1], 'r') as input_file:
        data = yaml.safe_load(input_file)
    
    number_of_cells, cells = parse_yaml(data)
    total_gold, dragon_positions = solve_problem(number_of_cells, cells)
    print(format_result(total_gold, dragon_positions))


if __name__ == "__main__":
    main()