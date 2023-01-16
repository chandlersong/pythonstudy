import unittest
from unittest import TestCase

import pandas as pd
import numpy as np

class CompareTest(TestCase):

    def setUp(self):
        self.df = pd.DataFrame({'one': pd.Series(np.random.randn(3), index=['a', 'b', 'c']),
                           'two': pd.Series(np.random.randn(4), index=['a', 'b', 'c', 'd']),
                           'three': pd.Series(np.random.randn(3), index=['b', 'c', 'd'])})

        print(self.df)
        self.series = pd.Series(np.random.randn(4), index=['one', 'two', 'three', 'four'])
        print(self.series)

    def test_compare_borast(self):
        print(self.df.gt(self.series))


if __name__ == '__main__':
    unittest.main()