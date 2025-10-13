import unittest
from solution import max_gold_with_dragons, Cell

class TestMaxGoldWithDragons(unittest.TestCase):

    # --- Basic Cases ---
    def test_sample_case(self):
        n = 6
        cells = [
            Cell('d', 10),
            Cell('d', 12),
            Cell('p', 2),
            Cell('d', 1),
            Cell('p', 2),
        ]
        total_gold, dragons = max_gold_with_dragons(n, cells)
        self.assertEqual(total_gold, 13)
        self.assertEqual(dragons, [3, 5])

    def test_enough_dragons_to_satisfy_beauty_requirements(self):
        n = 5
        cells = [
            Cell('d', 5),
            Cell('p', 3),
            Cell('d', 1),
            Cell('p', 2),
        ]
        total_gold, dragons = max_gold_with_dragons(n, cells)
        self.assertEqual(total_gold, 6)
        self.assertEqual(dragons, [2, 4])

    # --- Impossible Cases ---
    def test_impossible_case_due_to_insufficient_dragons(self):
        n = 6
        cells = [
            Cell('d', 10),
            Cell('d', 12),
            Cell('p', 2),
            Cell('d', 1),
            Cell('p', 3),
        ]
        result = max_gold_with_dragons(n, cells)
        self.assertIsNone(result)

    def test_no_dragons(self):
        n = 3
        cells = [
            Cell('p', 1),
            Cell('p', 1),
        ]
        result = max_gold_with_dragons(n, cells)
        self.assertIsNone(result)

    def test_all_small_dragons(self):
        n = 6
        cells = [
            Cell('d', 1),
            Cell('d', 1),
            Cell('p', 2),
            Cell('d', 1),
            Cell('p', 3),
        ]
        result = max_gold_with_dragons(n, cells)
        self.assertIsNone(result)

    def test_last_princess_requires_more_than_available(self):
        n = 5
        cells = [
            Cell('d', 3),
            Cell('p', 1),
            Cell('d', 4),
            Cell('p', 3),
        ]
        result = max_gold_with_dragons(n, cells)
        self.assertIsNone(result)

    def test_equal_strength_dragons(self):
        n = 5
        cells = [
            Cell('d', 5),
            Cell('d', 5),
            Cell('p', 2),
            Cell('p', 2),
        ]
        result = max_gold_with_dragons(n, cells)
        self.assertIsNone(result)

    # --- Edge and Unique Cases ---
    def test_princess_first_in_list(self):
        n = 5
        cells = [
            Cell('p', 2),
            Cell('d', 5),
            Cell('d', 6),
            Cell('p', 1),
        ]
        total_gold, dragons = max_gold_with_dragons(n, cells)
        self.assertEqual(total_gold, 11)
        self.assertEqual(dragons, [3, 4])

    def test_only_dragons_before_last_princess(self):
        n = 5
        cells = [
            Cell('d', 5),
            Cell('d', 10),
            Cell('d', 7),
            Cell('p', 2),
        ]
        total_gold, dragons = max_gold_with_dragons(n, cells)
        self.assertEqual(total_gold, 22)
        self.assertEqual(dragons, [2, 3, 4])

    # --- Complex Scenario ---
    def test_multiple_dragons_and_princesses(self):
        n = 9
        cells = [
            Cell('d', 5),
            Cell('d', 10),
            Cell('d', 7),
            Cell('p', 2),
            Cell('d', 8),
            Cell('d', 12),
            Cell('d', 3),
            Cell('p', 3),
        ]
        total_gold, dragons = max_gold_with_dragons(n, cells)
        self.assertEqual(total_gold, 33)
        self.assertEqual(dragons, [3, 6, 7, 8])


if __name__ == '__main__':
    unittest.main()
