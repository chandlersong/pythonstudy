import datetime
import unittest
from unittest import TestCase

import pandas_datareader.data as web
from pyalgotrade.barfeed import googlefeed
from pyalgotrade.technical import rsi, ma
from pyalgotrade.tools import googlefinance

from pyalgotrade import strategy


class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        super(MyStrategy, self).__init__(feed)
        self.__rsi = rsi.RSI(feed[instrument].getCloseDataSeries(), 14)
        self.__sma = ma.SMA(self.__rsi, 15)
        self.__instrument = instrument

    def onBars(self, bars):
        bar = bars[self.__instrument]
        self.info("%s %s %s" % (bar.getClose(), self.__rsi[-1], self.__sma[-1]))


class TestLoadData(TestCase):
    def test_load_data(self):
        googlefinance.download_daily_bars('orcl', 2000, 'orcl-2000.csv')

    def test_pandas_datareader(self):
        start = datetime.datetime(2000, 1, 1)
        end = datetime.datetime(2000, 12, 31)
        shanghai = web.DataReader('orcl', 'yahoo', start, end)
        shanghai.to_json('test1.json')

    def run_strategy(self):
        # Load the yahoo feed from the CSV file
        feed = googlefeed.Feed()
        feed.addBarsFromCSV("orcl", "orcl-2000.csv")

        # Evaluate the strategy with the feed's bars.
        myStrategy = MyStrategy(feed, "orcl")
        myStrategy.run()


if __name__ == '__main__':
    unittest.main()
