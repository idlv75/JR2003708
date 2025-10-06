import unittest
import main
import sys


class TestMain(unittest.TestCase):

    def test_non_existing_file(self):
        sys.argv = ["main.py", "non_existing_file.yaml"]
        try:
            main.load_data()
            self.fail("Program should've exit")
        except SystemExit:
            pass
    
    def test_example_data(self):
        n, cells = main.load_data()
        self.assertEqual(n, 6)
        self.assertEqual(cells[0], ('d', 10))
        self.assertEqual(cells[-1], ('p', 2))

    def test_main_result(self):
        result = main.main()
        self.assertEqual(result, 1)

if __name__ == '__main__':
    unittest.main()