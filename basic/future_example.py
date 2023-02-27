import datetime
import unittest

import backtrader as bt
import pandas as pd
from backtrader import Order
from backtrader.feeds import PandasData
from loguru import logger

from basic.future import FutureComm


class TestFutureStrategy(bt.Strategy):

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

            # Check if an order has been completed
            # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                logger.info('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                margin = order.executed.margin
                if margin is None:
                    margin = -1
                logger.info('SELL EXECUTED, %.2f,Margin is %.2f' % (order.executed.price, margin))
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            logger.info('Order Canceled/Margin/Rejected')

    def next(self):
        date = bt.num2date(self.data.datetime[0])
        logger.info(f'{date},当前可用资金 {self.broker.getcash()},close is {self.data[0]}')
        logger.info(f'{date},当前总资产 {self.broker.getvalue()}')
        logger.info(f'{date} 当前持仓量 {self.broker.getposition(self.data).size}')

        if date.day == 1:
            self.sell(size=1, price=1, exectype=Order.Limit)
        # if date.day == 2:
        #     self.buy(size=2)


class FutureCase(unittest.TestCase):
    def test_future(self):
        price = []
        for i in range(1, 10):
            value = i * 10
            price.append([value, 1.1 * value, 0.9 * value, value, value * 100])
        cerebro = bt.Cerebro()
        broker = cerebro.broker
        broker.setcash(100.0)
        broker.addcommissioninfo(FutureComm(leverage=1, commission=0))
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
