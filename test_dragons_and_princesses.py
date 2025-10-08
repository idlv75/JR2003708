#!/usr/bin/env python3
"""
Unit tests for the Dragons and Princesses problem solution.
"""

import unittest
from dragons_and_princesses import DragonsAndPrincessesSolver, Cell, read_yaml_input


class TestDragonsAndPrincesses(unittest.TestCase):
    """Test cases for the Dragons and Princesses solver."""
    
    def test_simple_case(self):
        """Test a simple case with one dragon and one princess."""
        cells = [
            Cell(cell_type='d', value=10, position=2),
            Cell(cell_type='p', value=1, position=3)
        ]
        solver = DragonsAndPrincessesSolver(cells)
        result = solver.solve()
        
        self.assertIsNotNone(result)
        total_gold, killed_dragons = result
        self.assertEqual(total_gold, 10)
        self.assertEqual(len(killed_dragons), 1)
        self.assertEqual(killed_dragons, [2])
    
    def test_no_solution_case(self):
        """Test a case with no solution."""
        cells = [
            Cell(cell_type='d', value=5, position=2),
            Cell(cell_type='p', value=2, position=3)
        ]
        solver = DragonsAndPrincessesSolver(cells)
        result = solver.solve()
        
        self.assertIsNone(result)
    
    def test_multiple_dragons_princesses(self):
        """Test a case with multiple dragons and princesses."""
        cells = [
            Cell(cell_type='d', value=10, position=2),
            Cell(cell_type='p', value=1, position=3),
            Cell(cell_type='d', value=5, position=4),
            Cell(cell_type='p', value=1, position=5)
        ]
        solver = DragonsAndPrincessesSolver(cells)
        result = solver.solve()
        
        self.assertIsNotNone(result)
        total_gold, killed_dragons = result
        # The algorithm only needs to satisfy the last princess (position 5) with beauty 1
        # So it only needs to kill 1 dragon
        self.assertEqual(len(killed_dragons), 1)
        # The algorithm chooses the dragon in the final segment (position 4)
        self.assertIn(4, killed_dragons)
    
    def test_no_princesses(self):
        """Test a case with no princesses."""
        cells = [
            Cell(cell_type='d', value=10, position=2),
            Cell(cell_type='d', value=5, position=3)
        ]
        solver = DragonsAndPrincessesSolver(cells)
        result = solver.solve()
        
        self.assertIsNone(result)
    
    def test_empty_cells(self):
        """Test a case with empty cells."""
        cells = []
        solver = DragonsAndPrincessesSolver(cells)
        result = solver.solve()
        
        self.assertIsNone(result)
    
    def test_yaml_input_reading(self):
        """Test reading input from YAML file."""
        try:
            cells = read_yaml_input('test_input.yaml')
            
            self.assertEqual(len(cells), 1)
            self.assertEqual(cells[0].cell_type, 'd')
            self.assertEqual(cells[0].value, 10)
            self.assertEqual(cells[0].position, 2)
        except ImportError:
            self.skipTest("PyYAML not available")


if __name__ == '__main__':
    unittest.main()
