import unittest
import pandas as pd


class MultiIndexCase(unittest.TestCase):
    def test_rename_index(self):
        data = pd.DataFrame({"x": [1, 2, 3, 4, 5], "y": [6, 7, 8, 9, 0]},
                            index=(pd.MultiIndex.from_tuples(
                                [("a", "001"), ("a", "002"), ("a", "003"), ("b", "001"), ("b", "002")])))
        data = data.rename_axis(["c", "d"])
        print(data)
        print(data.reset_index())


if __name__ == '__main__':
    unittest.main()
