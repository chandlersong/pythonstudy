import tempfile
import unittest
import os
import pandas as pd
import shutil
from unittest import TestCase

from numpy.matlib import randn
from pandas import DataFrame


class TestDataFrameExample(TestCase):
    def setUp(self):
        self.example = DataFrame(randn(5, 2), index=range(0, 10, 2), columns=list('AB'))
        print("example data")
        print("========================================================================")
        print(self.example)
        print("========================================================================")

    def test_loop_1(self):
        data = self.example.to_records()
        record = data[0]
        print(type(record))
        print(record.A)

    def test_loop_2(self):
        for index, row in self.example.iterrows():
            print(index)
            print(type(index))
            print(row)
            print(type(row))

    def test_add_column(self):
        self.example['new column'] = range(5)
        print(self.example)

    def test_to_csv(self):
        testfileName = tempfile.gettempdir() + "\\test"

        if os.path.exists(testfileName):
            shutil.rmtree(testfileName)
        os.mkdir(testfileName)
        testfileName = testfileName +"\\a.csv"
        print(testfileName)

        self.example.to_csv(testfileName,compression="gzip")
        print(pd.read_csv(testfileName,index_col=0,compression="gzip"))


if __name__ == '__main__':
    unittest.main()
