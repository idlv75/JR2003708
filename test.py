import unittest
import main

class Tests(unittest.TestCase):
    def setUp(self):
        self.data= {
            'given_example_1': [{'number_of_cells': 6}, {'game': ['d 10', 'd 12', 'p 2', 'd 1', 'p 2']}, {'expected': '13\n2\n3 5'}],
            'given_example_2': [{'number_of_cells': 6}, {'game': ['d 10', 'd 12', 'p 2', 'd 1', 'p 3']}, {'expected': '-1'}],
            'multiple_options': [{'number_of_cells': 7}, {'game': ['d 10', 'd 12', 'd 12', 'p 2', 'd 1', 'p 2']}, {'expected': '13\n2\n3 6\n\n\n13\n2\n4 6'}],
            'unknown_data_type': [{'number_of_cells': 3}, {'game': ['t 3', 'p 2', 'd 1']}],
            'non_numeric_input': [{'number_of_cells': 'd'}, {'game': ['d bob', 'p', 'd 1']}],
            'an_empty_game': None,
            'princess_not_on_last_cell': [{'number_of_cells': 4}, {'game': ['d 3', 'p 2', 'd 1']}],
            'large_numbers': [{'number_of_cells': 6}, {'game': ['p 10000', 'd 10000', 'p 9999', 'd 1', 'p 8000']}, {'expected': '-1'}],
            'large_numbers_2': [{'number_of_cells': 6}, {'game': ['p 10000', 'd 10000', 'p 9999', 'd 1', 'p 10000']}, {'expected': '-1'}],
            'negative_beauty': [{'number_of_cells': 6}, {'game': ['p -10000', 'd 10000', 'p 9999', 'd 1', 'p 10000']}, {'expected': '-1'}],
            'negative_gold': [{'number_of_cells': 6}, {'game': ['p 10000', 'd -10000', 'p 9999', 'd 1', 'p 10000']}, {'expected': '-1'}],
        }
        
    def test_example_1(self):
        self.assertTrue(main.solve("tests.yaml","given_example_1",self.data),self.data["given_example_1"][2]["expected"])
    def test_example_2(self):
        self.assertTrue(main.solve("tests.yaml","given_example_2",self.data),self.data["given_example_2"][2]["expected"])
    def test_multiple_options(self):
        self.assertTrue(main.solve("tests.yaml","multiple_options",self.data),self.data["multiple_options"][2]["expected"])
    def test_unknown_data_type(self):
        with self.assertRaises(Exception):
            main.solve("tests.yaml","unknown_data_type",self.data)
    def test_non_numeric_input(self):
        with self.assertRaises(Exception):
            main.solve("tests.yaml","non_numeric_input",self.data)
    def test_empty_game(self):
        with self.assertRaises(Exception):
            main.solve("tests.yaml","an_empty_game",self.data)
    def test_negative_beauty(self):
        with self.assertRaises(Exception):
            main.solve("tests.yaml","negative_beauty",self.data)
    def test_negative_gold(self):
        with self.assertRaises(Exception):
            main.solve("tests.yaml","negative_gold",self.data)
    def test_princess_not_on_last_cell(self):
        with self.assertRaises(Exception):
            main.solve("tests.yaml","princess_not_on_last_cell",self.data)
    def test_large_numbers(self):
        self.assertTrue(main.solve("tests.yaml","large_numbers",self.data),self.data["large_numbers"][2]["expected"])
    def test_large_numbers_2(self):
        self.assertTrue(main.solve("tests.yaml","large_numbers_2",self.data),self.data["large_numbers_2"][2]["expected"])

if __name__=="__main__":
    unittest.main()

