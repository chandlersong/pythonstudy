import unittest
from unittest import TestCase

from pyalgotrade.barfeed import googlefeed
from pyalgotrade.broker import slippage
from pyalgotrade.broker.backtesting import TradePercentage, Broker
from pyalgotrade.broker.fillstrategy import DefaultStrategy
from pyalgotrade.stratanalyzer import trades

from pyalgotradeStudy.Strategy import SimpleStrategy


class TestBoker(TestCase):
    def test_hello_world(self):
        feed = googlefeed.Feed()
        feed.addBarsFromCSV("orcl", "orcl-2000.csv")

        broker_commission = TradePercentage(0.0001)

        # 3.2 fill strategy设置
        fill_stra = DefaultStrategy(volumeLimit=0.1)
        sli_stra = slippage.NoSlippage()
        fill_stra.setSlippageModel(sli_stra)

        brk = Broker(1000000, feed, broker_commission)

        myStrategy = SimpleStrategy(feed, "orcl", 15, brk)

        trade_situation = trades.Trades()
        myStrategy.attachAnalyzer(trade_situation)

        myStrategy.run()

        print("Final portfolio value: %s" % myStrategy.getBroker().getEquity())
        print("commissions : %s" % trade_situation.getCommissionsForAllTrades())


if __name__ == '__main__':
    unittest.main()
