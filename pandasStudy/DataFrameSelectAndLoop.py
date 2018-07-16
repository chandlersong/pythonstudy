import os
import shutil
import tempfile
import unittest
from unittest import TestCase
from urllib import request

import pandas as pd
from numpy.matlib import randn
from pandas import DataFrame
from pandas.util.testing import assert_series_equal, assert_frame_equal


class TestDataFrameExample(TestCase):
    def setUp(self):
        self.example = DataFrame(randn(5, 2), index=range(0, 10, 2), columns=list('AB'))
        print("example data")
        print("========================================================================")
        print(self.example)
        print("========================================================================")

    def test_empty(self):

        empty = DataFrame()

        if   empty.empty:
            print("empty \n")
        else:
            print("not empty \n")


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
        testfileName = testfileName + "\\a.csv"
        print(testfileName)

        self.example.to_csv(testfileName, compression="gzip")
        print(pd.read_csv(testfileName, index_col=0, compression="gzip"))

    def test_read_csv_from_internet(self):
        latest_report = '2018-03-31'
        index_col = 0

        with request.urlopen('http://quotes.money.163.com/service/zcfzb_600073.html') as web:
            local = pd.read_csv(web, encoding='gb2312', na_values='--', index_col=index_col)
            result = local.drop(local.columns[len(local.columns) - 1], axis=1).fillna(0)
            print(result[latest_report])

        with request.urlopen('http://quotes.money.163.com/service/xjllb_600073.html') as web:
            local = pd.read_csv(web, encoding='gb2312', na_values='--', index_col=index_col)
            result = local.drop(local.columns[len(local.columns) - 1], axis=1).fillna(0)
            print(result[latest_report])

        with request.urlopen('http://quotes.money.163.com/service/lrb_600073.html') as web:
            local = pd.read_csv(web, encoding='gb2312', na_values='--', index_col=index_col)
            result = local.drop(local.columns[len(local.columns) - 1], axis=1).fillna(0)
            print(result[latest_report])

    def test_read_csv_save(self):
        latest_report = '2018-03-31'
        index_col = 0

        with request.urlopen('http://quotes.money.163.com/service/zcfzb_600073.html') as web:
            local = pd.read_csv(web, encoding='gb2312', na_values='--', index_col=index_col)
            print(local.shape)
            result = local.drop(local.columns[len(local.columns) - 1], axis=1).fillna(0).apply(pd.to_numeric,
                                                                                               errors='coerce')

            testfileName = tempfile.gettempdir() + "\\test"

            if os.path.exists(testfileName):
                shutil.rmtree(testfileName)
            os.mkdir(testfileName)
            testfileName = testfileName + "\\a.csv"
            print(testfileName)
            result.to_csv(testfileName, encoding='utf-8')

            actual = pd.read_csv(testfileName, index_col=0).apply(pd.to_numeric, args=('coerce',))
            print(actual[latest_report])
            print(result[latest_report])

            print(result.shape)
            print(actual.shape)

            print(result.columns)

            assert_series_equal(result[latest_report], actual[latest_report], check_dtype=False)
            assert_frame_equal(result, actual)

        with request.urlopen('http://quotes.money.163.com/service/zcfzb_600096.html') as web:
            origin = pd.read_csv(web,  encoding='gb2312')
            origin.to_csv(tempfile.gettempdir() + "\\test\\600096.csv")

        print(tempfile.gettempdir() + "\\test")

if __name__ == '__main__':
    unittest.main()
