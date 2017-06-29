import datetime
import unittest
from unittest import TestCase

from pyalgotrade import bar, strategy
from pyalgotrade.bar import BasicBar
from pyalgotrade.barfeed import membf
from pyalgotrade.technical import rsi, ma

import pandas as pd


class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        super(MyStrategy, self).__init__(feed)
        self.__rsi = rsi.RSI(feed[instrument].getCloseDataSeries(), 14)
        self.__sma = ma.SMA(self.__rsi, 15)
        self.__instrument = instrument

    def onBars(self, bars):
        bar = bars[self.__instrument]
        self.info("%s %s %s" % (bar.getClose(), self.__rsi[-1], self.__sma[-1]))


class MyFeed(membf.BarFeed):
    def __init__(self, frequency=bar.Frequency.DAY, timezone=None, maxLen=None):
        if frequency not in [bar.Frequency.DAY]:
            raise Exception("Invalid frequency.")

        super(MyFeed, self).__init__(frequency, maxLen)

        self.__timezone = timezone
        self.__sanitizeBars = False
        self.__dateTimeFormat = "%d-%b-%y"

    def readFromPandas(self, instrument, df, timezone=None):
        loadedBars = []
        for index, row in df.iterrows():
            dateTime = self._parseDate(index)
            open_ = float(row[0])
            high = float(row[1])
            low = float(row[2])
            close = float(row[3])
            volume = float(row[4])
            bar_ = BasicBar(
                dateTime, open_, high, low, close, volume, None, bar.Frequency.DAY, extra={})

            loadedBars.append(bar_)

        self.addBarsFromSequence(instrument, loadedBars)

    def _parseDate(self, dateString):
        ret = datetime.datetime.strptime(dateString, self.__dateTimeFormat)


        return ret


class TestCustomFeed(TestCase):
    def setUp(self):
        self.data = pd.read_csv("orcl-2000.csv", index_col="Date")
        #print(self.data)

    def test_helloworld(self):
        feed = MyFeed()
        feed.readFromPandas("orcl", self.data)

        # Evaluate the strategy with the feed's bars.
        myStrategy = MyStrategy(feed, "orcl")
        myStrategy.run()


if __name__ == '__main__':
    unittest.main()
