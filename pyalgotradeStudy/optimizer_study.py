import unittest
from unittest import TestCase

import itertools

from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.optimizer import server, worker, local

from pyalgotradeStudy.Strategy import RSI2


def parameters_generator():
    instrument = ["dia"]
    entrySMA = range(150, 251)
    exitSMA = range(5, 16)
    rsiPeriod = range(2, 11)
    overBoughtThreshold = range(75, 96)
    overSoldThreshold = range(5, 26)
    return itertools.product(instrument, entrySMA, exitSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold)


class TestOptimizer(TestCase):

    def test_server_client(self):
        # Load the feed from the CSV files.
        feed = yahoofeed.Feed()
        feed.addBarsFromCSV("dia", "data/DIA-2010-yahoofinance.csv")
        feed.addBarsFromCSV("dia", "data/DIA-2011-yahoofinance.csv")
        feed.addBarsFromCSV("dia", "data/DIA-2012-yahoofinance.csv")

        # Run the server.
        server.serve(feed, parameters_generator(), "localhost", 5000)

    def test_client_run(self):
        worker.run(RSI2, "localhost", 5000, workerName="localworker")

    def test_local(self):
        feed = yahoofeed.Feed()
        feed.addBarsFromCSV("dia", "data/DIA-2010-yahoofinance.csv")
        feed.addBarsFromCSV("dia", "data/DIA-2011-yahoofinance.csv")
        feed.addBarsFromCSV("dia", "data/DIA-2012-yahoofinance.csv")

        local.run(RSI2, feed, parameters_generator())

# The if __name__ == '__main__' part is necessary if running on Windows.
if __name__ == '__main__':
    unittest.main()