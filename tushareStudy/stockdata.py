import tempfile
import unittest
import pandas as pd
from unittest import TestCase

import os

import shutil
import tushare as ts
from pandas.util.testing import assert_frame_equal


class TencentData(TestCase):
    def setUp(self):
        print(ts.__version__)

    def test_load_data(self):
        print("前复权")
        print(ts.get_k_data('600000', start='2016-10-20', end='2016-10-31'))
        print("后复权")
        print(ts.get_k_data('600000', start='2016-10-20', end='2016-10-31', autype='hfq'))
        print("不复权")
        print(ts.get_k_data('600000', start='2016-10-20', end='2016-10-31', autype=None))
        print("2016-10-20 5分钟")
        print(ts.get_k_data('600000', start='2016-10-20', end='2016-10-20', ktype='5', autype=None))
        print("2016-10-20 30分钟")
        print(ts.get_k_data('600000', start='2016-10-20', end='2016-10-21', ktype='30', autype=None))


    def test_5_m_mins_data(self):
        print("2016-10-20 5分钟")
        print(ts.get_k_data('600000', start='2016-10-20', end='2016-10-20', ktype='5', autype=None))

    def test_load_data_qfq(self):
        print("前复权")
        print(ts.get_k_data('600096', start='2018-04-12', end='2018-04-13'))

    def test_5_min_data(self):
        print("2016-10-20 5分钟")
        print(ts.get_k_data('600000', ktype='5'))


class SinaData(TestCase):
    def setUp(self):
        print(ts.__version__)

    def test_load_hist_data(self):
        print(ts.get_h_data('600096',start='2017-06-21', end='2017-06-30'))

    def test_load_hist_data(self):
        data = ts.get_hist_data('600096', start='2017-06-21', end='2017-06-30')
        print(data)


class SinaData(TestCase):
    def setUp(self):
        print(ts.__version__)

    def test_load_hist_data(self):
        print(ts.get_h_data('600000',start='2017-06-21', end='2017-06-30'))

class SinaData(TestCase):
    def setUp(self):
        print(ts.__version__)

    def test_load_hist_data_to_csv(self):
        testfileName = tempfile.gettempdir() + "\\test"

        if os.path.exists(testfileName):
            shutil.rmtree(testfileName)
        os.mkdir(testfileName)
        testfileName = testfileName + "\\sina.csv"
        print(testfileName)

        data = ts.get_h_data('600000', start='2017-06-28', end='2017-06-30')
        data.to_csv(testfileName, compression="gzip")
        reader_data = pd.read_csv(testfileName, index_col=0, compression="gzip",parse_dates=True)
        print(reader_data)

        assert_frame_equal(data,reader_data)


class DataEyes(TestCase):
    def setUp(self):
        ts.set_token("5244a7ac2b89c58102d13f5c54975aa09a6086217dea64ce6ee13404cc7390bd")

    def test_hello_world(self):
        mt = ts.Master()
        df = mt.TradeCal(exchangeCD='XSHG', beginDate='20150928', endDate='20151010',
                         field='calendarDate,isOpen,prevTradeDate')
        print(df)


if __name__ == '__main__':
    unittest.main()
