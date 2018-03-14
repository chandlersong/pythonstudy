import unittest
from unittest import TestCase

from pyalgotrade.barfeed import googlefeed
from pyalgotrade.stratanalyzer import returns

from pyalgotradeStudy.Strategy import SimpleStrategy


def run_strategy(smaPeriod):
    # Load the yahoo feed from the CSV file
    feed = googlefeed.Feed()
    feed.addBarsFromCSV("orcl", "orcl-2000.csv")

    # Evaluate the strategy with the feed.
    myStrategy = SimpleStrategy(feed, "orcl", smaPeriod)
    returnsAnalyzer = returns.Returns()
    myStrategy.attachAnalyzer(returnsAnalyzer)

    myStrategy.run()

    broker = myStrategy.getBroker()
    print("Final portfolio value: $%.2f" % broker.getEquity())
    print(dir(broker))
    print("getPositions:{}".format(broker.getPositions()))
    print("getActiveOrder:{}".format(broker.getActiveOrders()))


class Test_Trade(TestCase):
    def test_hello_world(self):
        run_strategy(15)


if __name__ == '__main__':
    unittest.main()
