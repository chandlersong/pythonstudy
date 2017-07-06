import unittest
from unittest import TestCase

import tushare as ts


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

    def test_load_data_qfq(self):
        print("前复权")
        print(ts.get_k_data('600000', start='2017-06-21', end='2017-06-30'))

    def test_5_min_data(self):
        print("2016-10-20 5分钟")
        print(ts.get_k_data('600000', ktype='5'))


class SinaData(TestCase):
    def setUp(self):
        print(ts.__version__)

    def test_load_hist_data(self):
        print(ts.get_h_data('600000',start='2017-06-21', end='2017-06-30'))


if __name__ == '__main__':
    unittest.main()
