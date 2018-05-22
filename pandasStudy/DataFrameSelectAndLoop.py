import os
import shutil
import tempfile
import unittest
from unittest import TestCase
from urllib import request

import pandas as pd
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

    def test_read_csv_from_internet(self):
        latest_report = '2018-03-31'
        index_col = 0

        with request.urlopen('http://quotes.money.163.com/service/zcfzb_600073.html') as web:
            local = pd.read_csv(web, encoding='gb2312', na_values='--',index_col=index_col)
            result = local.drop(local.columns[len(local.columns) - 1], axis=1).fillna(0)
            print(result[latest_report])

        with request.urlopen('http://quotes.money.163.com/service/xjllb_600073.html') as web:
            local = pd.read_csv(web, encoding='gb2312', na_values='--',index_col=index_col)
            result = local.drop(local.columns[len(local.columns) - 1], axis=1).fillna(0)
            print(result[latest_report])

        with request.urlopen('http://quotes.money.163.com/service/lrb_600073.html') as web:
            local = pd.read_csv(web, encoding='gb2312', na_values='--', index_col=index_col)
            result = local.drop(local.columns[len(local.columns) - 1], axis=1).fillna(0)
            print(result[latest_report])


if __name__ == '__main__':
    unittest.main()
