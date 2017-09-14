import unittest
from unittest import TestCase

import numpy as np
import talib
from talib import MA_Type, MA


class Test_Trade(TestCase):
    def test_sma(self):
        close = np.random.random(100)
        output = talib.SMA(close)
        print(output)

    def test_ma_type(self):
        close = np.random.random(100)
        upper, middle, lower = talib.BBANDS(close, matype=MA_Type.T3)
        print("upper:")
        print(upper)
        print("middle:")
        print(middle)
        print("lower:")
        print(lower)

    def test_ma(self):
        close = np.random.random(100)
        real = MA(close, timeperiod=30, matype=0)


if __name__ == '__main__':
    unittest.main()