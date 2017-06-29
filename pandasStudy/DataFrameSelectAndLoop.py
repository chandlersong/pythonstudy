import unittest
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

    def loop_1(self):
        data =  self.example.to_records()
        record = data[0]
        print(type(record))
        print(record.A)

    def loop_2(self):
        for index,row in self.example.iterrows():
            print(index)
            print(type(index))
            print(row)
            print(type(row))

if __name__ == '__main__':
    unittest.main()