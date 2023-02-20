import datetime
import sys
import unittest
import backtrader as bt
import pandas as pd
from backtrader.feeds import PandasData
from loguru import logger

from basic.Bbands import BbandsStrategy


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        logger.remove()
        logger.add(sys.stderr, level="INFO")  # or sys.stdout or other file object
        logger.add(f"logs/log_{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log",
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
        cerebro.adddata(bt_data)
        cerebro.addstrategy(BbandsStrategy, period=5, bias=1.1)
        cerebro.run()
        logger.info(f'Final Portfolio value: {cerebro.broker.getvalue()}')
        logger.info(f'Final Portfolio cash: {cerebro.broker.getcash()}')
        logger.info(f'Final Portfolio position size: {cerebro.broker.getposition(0).size}')


if __name__ == '__main__':
    unittest.main()
