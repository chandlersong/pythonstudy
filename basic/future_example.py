import datetime
import unittest

import pandas as pd
import backtrader as bt
from loguru import logger
from backtrader.feeds import PandasData


class TestFutureStrategy(bt.Strategy):

    def next(self):
        date = bt.num2date(self.data.datetime[0])
        if date.day == 2:
            self.sell()

        if date.day == 5:
            self.close()


class FutureCase(unittest.TestCase):
    def test_something(self):
        data = compose_test_data()
        cerebro = bt.Cerebro()
        broker = cerebro.broker
        broker.setcash(100.0)
        cerebro.adddata(data)
        cerebro.addstrategy(TestFutureStrategy)
        cerebro.run()
        logger.info('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())


def compose_test_data() -> PandasData:
    start = datetime.datetime(2023, 12, 1)
    res = []
    for i in range(1, 10):
        value = 10-i
        res.append([start + datetime.timedelta(days=i), value, 1.1 * value, 0.9 * value, value, value])

    return PandasData(dataname=pd.DataFrame(res, columns=['datetime', 'open', 'high', 'low', 'close', 'volume']),
                      datetime='datetime',
                      high='high',
                      low='low',
                      open='open',
                      close='close',
                      volume='volume')


if __name__ == '__main__':
    unittest.main()
