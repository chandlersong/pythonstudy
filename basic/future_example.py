import datetime
import unittest

import pandas as pd
import backtrader as bt
from loguru import logger
from backtrader.feeds import PandasData


class TestFutureStrategy(bt.Strategy):
    def next(self):
        date = bt.num2date(self.data.datetime[0])
        logger.info(f'{date},当前可用资金 {self.broker.getcash()},close is {self.data[0]}')
        logger.info(f'{date},当前总资产 {self.broker.getvalue()}')
        logger.info(f'{date} 当前持仓量 {self.broker.getposition(self.data).size}')

        if date.day == 2:
            self.sell(size=2)

        # if date.day == 5:
        #     self.close()


class FutureCase(unittest.TestCase):
    def test_something(self):
        price = []
        for i in range(1, 10):
            value = i
            price.append([value, 1.1 * value, 0.9 * value, value, value * 100])
        cerebro = bt.Cerebro()
        broker = cerebro.broker
        broker.setcash(100.0)
        broker.setcommission(
            commtype=bt.CommInfoBase.COMM_PERC,
            mult=3.0,
            stocklike=False,
            automargin=0.1
        )
        cerebro.adddata(compose_test_data(price))
        cerebro.addstrategy(TestFutureStrategy)
        cerebro.run()
        logger.info('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())


def compose_test_data(price) -> PandasData:
    start = datetime.datetime(2023, 12, 1)
    for idx, p in enumerate(price):
        p.insert(0, start + datetime.timedelta(days=idx))
    data = pd.DataFrame(price, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    logger.info("prices:===========================")
    logger.info(data)
    logger.info("prices:===========================")
    return PandasData(dataname=data,
                      datetime='datetime',
                      high='high',
                      low='low',
                      open='open',
                      close='close',
                      volume='volume')


if __name__ == '__main__':
    unittest.main()
