#!/usr/bin/env python3

import unittest
from solution import (
    Cell, Dragon, Princess,
    parse_yaml, split_entities,
    is_valid_selection, find_best_dragons,
    solve_problem, format_result
)


class TestImmutability(unittest.TestCase):
    
    def test_dragon_frozen(self):
        dragon = Dragon(position=2, gold=10)
        with self.assertRaises(AttributeError):
            dragon.gold = 20
    
    def test_princess_frozen(self):
        princess = Princess(position=3, beauty=2)
        with self.assertRaises(AttributeError):
            princess.beauty = 5
    
    def test_cell_frozen(self):
        cell = Cell(position=2, cell_type='d', value=10)
        with self.assertRaises(AttributeError):
            cell.value = 20


class TestParsing(unittest.TestCase):
    
    def test_parse_yaml(self):
        data = {
            'n': 3,
            'cells': [
                {'type': 'd', 'value': 10},
                {'type': 'p', 'value': 1}
            ]
        }
        number_of_cells, cells = parse_yaml(data)
        
        self.assertEqual(number_of_cells, 3)
        self.assertEqual(len(cells), 2)
        self.assertEqual(cells[0].cell_type, 'd')
        self.assertEqual(cells[0].value, 10)
        self.assertEqual(cells[0].position, 2)
    
    def test_split_entities(self):
        cells = (
            Cell(position=2, cell_type='d', value=10),
            Cell(position=3, cell_type='d', value=12),
            Cell(position=4, cell_type='p', value=2),
            Cell(position=5, cell_type='d', value=1),
            Cell(position=6, cell_type='p', value=2),
        )
        
        dragons, princesses = split_entities(cells)
        
        self.assertEqual(len(dragons), 3)
        self.assertEqual(len(princesses), 2)
        self.assertEqual(dragons[0].gold, 10)
        self.assertEqual(princesses[0].beauty, 2)


class TestConstraints(unittest.TestCase):
    
    def test_valid_selection(self):
        dragons = (
            Dragon(position=2, gold=10),
            Dragon(position=3, gold=12),
            Dragon(position=5, gold=1),
        )
        princesses = (Princess(position=4, beauty=2),)
        selected_indices = {0, 2}
        
        self.assertTrue(is_valid_selection(dragons, princesses, selected_indices))
    
    def test_invalid_selection(self):
        dragons = (
            Dragon(position=2, gold=10),
            Dragon(position=3, gold=12),
            Dragon(position=5, gold=1),
        )
        princesses = (Princess(position=4, beauty=2),)
        selected_indices = {0, 1}
        
        self.assertFalse(is_valid_selection(dragons, princesses, selected_indices))
    
    def test_no_constraints(self):
        dragons = (
            Dragon(position=2, gold=10),
            Dragon(position=3, gold=12),
        )
        princesses = ()
        selected_indices = {0, 1}
        
        self.assertTrue(is_valid_selection(dragons, princesses, selected_indices))


class TestSolution(unittest.TestCase):
    
    def test_example1(self):
        cells = (
            Cell(position=2, cell_type='d', value=10),
            Cell(position=3, cell_type='d', value=12),
            Cell(position=4, cell_type='p', value=2),
            Cell(position=5, cell_type='d', value=1),
            Cell(position=6, cell_type='p', value=2),
        )
        
        total_gold, dragon_positions = solve_problem(6, cells)
        
        self.assertEqual(total_gold, 13)
        self.assertEqual(len(dragon_positions), 2)
        self.assertIn(3, dragon_positions)
        self.assertIn(5, dragon_positions)
    
    def test_example2_impossible(self):
        cells = (
            Cell(position=2, cell_type='d', value=10),
            Cell(position=3, cell_type='d', value=12),
            Cell(position=4, cell_type='p', value=2),
            Cell(position=5, cell_type='d', value=1),
            Cell(position=6, cell_type='p', value=3),
        )
        
        total_gold, dragon_positions = solve_problem(6, cells)
        
        self.assertEqual(total_gold, -1)
    
    def test_simple_case(self):
        cells = (
            Cell(position=2, cell_type='d', value=100),
            Cell(position=3, cell_type='p', value=1),
        )
        
        total_gold, dragon_positions = solve_problem(3, cells)
        
        self.assertEqual(total_gold, 100)
        self.assertEqual(dragon_positions, (2,))
    
    def test_zero_beauty(self):
        cells = (
            Cell(position=2, cell_type='d', value=50),
            Cell(position=3, cell_type='p', value=0),
        )
        
        total_gold, dragon_positions = solve_problem(3, cells)
        
        self.assertEqual(total_gold, 0)
        self.assertEqual(len(dragon_positions), 0)
    
    def test_multiple_same_gold(self):
        cells = (
            Cell(position=2, cell_type='d', value=10),
            Cell(position=3, cell_type='d', value=10),
            Cell(position=4, cell_type='d', value=10),
            Cell(position=5, cell_type='p', value=2),
        )
        
        total_gold, dragon_positions = solve_problem(5, cells)
        
        self.assertEqual(total_gold, 20)
        self.assertEqual(len(dragon_positions), 2)


class TestFormatting(unittest.TestCase):
    
    def test_format_success(self):
        output = format_result(100, (2, 5, 7))
        expected = "100\n3\n2 5 7"
        self.assertEqual(output, expected)
    
    def test_format_impossible(self):
        output = format_result(-1, ())
        self.assertEqual(output, "-1")
    
    def test_format_zero(self):
        output = format_result(0, ())
        expected = "0\n0"
        self.assertEqual(output, expected)


class TestEdgeCases(unittest.TestCase):
    
    def test_only_princess(self):
        cells = (Cell(position=2, cell_type='p', value=0),)
        total_gold, dragon_positions = solve_problem(2, cells)
        
        self.assertEqual(total_gold, 0)
    
    def test_all_dragons_before_princess(self):
        cells = (
            Cell(position=2, cell_type='d', value=5),
            Cell(position=3, cell_type='d', value=10),
            Cell(position=4, cell_type='d', value=15),
            Cell(position=5, cell_type='p', value=2),
        )
        
        total_gold, dragon_positions = solve_problem(5, cells)
        
        self.assertEqual(total_gold, 25)
        self.assertEqual(len(dragon_positions), 2)


if __name__ == '__main__':
    unittest.main()