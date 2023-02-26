import datetime
import sys
import unittest
import backtrader as bt
import pandas as pd
from backtrader.feeds import PandasData
from loguru import logger

from basic.Bbands import BbandsStrategy, ExportCSVtAnalysis
from basic.future import FutureComm


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        logger.remove()
        logger.add(sys.stderr, level="INFO")  # or sys.stdout or other file object
        self.timestamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        logger.add(f"logs/log_{self.timestamp}.log",
                   level="DEBUG")  # or sys.stdout or other file object

    def test_bbands(self):
        data = pd.read_csv("data.csv", parse_dates=['timestamp'], index_col='idx', date_parser=(
            lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H.%M.%S')))
        strategy_data = data.resample(rule='15T', on='timestamp').agg(
            {'open': 'first',
             'high': 'max',
             'low': 'min',
             'close': 'last',
             'volume': 'sum'
             })
        strategy_data = strategy_data.reset_index()
        bt_data = PandasData(dataname=strategy_data,
                             datetime='timestamp',
                             high='high',
                             low='low',
                             open='open',
                             close='close',
                             volume='volume')
        cerebro = bt.Cerebro()
        broker = cerebro.broker
        broker.setcash(1000000.0)
        broker.addcommissioninfo(FutureComm(leverage=3))
        cerebro.adddata(bt_data)
        cerebro.addanalyzer(ExportCSVtAnalysis, _name="csv")
        cerebro.addstrategy(BbandsStrategy, period=5, bias=1.1)
        strat = cerebro.run(runonce=True)
        logger.info(f'Final Portfolio profile: {cerebro.broker.getvalue() / 1000000.0}')
        logger.info(f'Final Portfolio cash: {cerebro.broker.getcash()}')
        logger.info(f'Final Portfolio position size: {cerebro.broker.getposition(0).size}')
        csv_export = strat[0].analyzers.csv
        analysis = csv_export.get_analysis()
        data = pd.DataFrame(analysis, columns=["timestamp", "open", "hign", "low", "close", "median", "upper", "lower",
                                               "signal", "position", "cash","value"])
        data.to_csv(f"logs/transaction_{self.timestamp}.csv")


if __name__ == '__main__':
    unittest.main()
