import datetime
import unittest

import pandas as pd
import backtrader as bt
from loguru import logger
from backtrader.feeds import PandasData


class TestFutureStrategy(bt.Strategy):
    params = (('period', 15))

    def __init__(self):
        self.sma = bt.indicators.SMA(self.data, period=self.p.period)

    def next(self):
        date = bt.num2date(self.data.datetime[0])
        if date.day == 2:
            self.sell()

        if date.day == 5:
            self.close()


class FutureCase(unittest.TestCase):
    def test_something(self):
        price = []
        for i in range(1, 10):
            value = 10 - i
            price.append([value, 1.1 * value, 0.9 * value, value, value * 100])
        cerebro = bt.Cerebro()
        broker = cerebro.broker
        broker.setcash(100.0)
        cerebro.adddata(compose_test_data(price))
        cerebro.addstrategy(TestFutureStrategy, period=[20, 25])
        cerebro.run()
        logger.info('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())


def compose_test_data(price) -> PandasData:
    start = datetime.datetime(2023, 12, 1)
    for idx, p in enumerate(price):
        p.insert(0, start + datetime.timedelta(days=idx))
    print(price)
    return PandasData(dataname=pd.DataFrame(price, columns=['datetime', 'open', 'high', 'low', 'close', 'volume']),
                      datetime='datetime',
                      high='high',
                      low='low',
                      open='open',
                      close='close',
                      volume='volume')


if __name__ == '__main__':
    unittest.main()
