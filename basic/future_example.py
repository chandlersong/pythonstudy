import datetime
import unittest

import backtrader as bt
import pandas as pd
from backtrader import Order
from backtrader.feeds import PandasData
from loguru import logger

from basic.Indicators import ProfitIndicator
from basic.future import FutureComm


class TestFutureStrategy(bt.Strategy):

    def __init__(self):
        self.pnl_check = ProfitIndicator(self.data, broker=self.broker)

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
        logger.info(f"pnl:{self.pnl_check.pnl[0]}")
        date = bt.num2date(self.data.datetime[0])
        logger.info(f'{date},当前可用资金 {self.broker.getcash()},close is {self.data[0]}')
        logger.info(f'{date},当前总资产 {self.broker.getvalue()}')
        position = self.broker.getposition(self.data)
        assert_value = position.size * (self.data.close[0] - position.price)
        logger.info(f'{date} 当前持仓量 {position.size},价格：{position.price},持仓价值：{assert_value}')
        if date.day == 1:
            self.sell(exectype=Order.Limit, size=1)
        if date.day == 2:
            self.sell(exectype=Order.Limit, size=3)


class FutureCase(unittest.TestCase):
    def test_future(self):
        price = []
        for i in range(1, 10):
            value = i * 10
            price.append([value, 1.1 * value, 0.9 * value, value, value * 100])
        cerebro = bt.Cerebro()
        broker = cerebro.broker
        broker.setcash(100.0)
        broker.addcommissioninfo(FutureComm(leverage=2, commission=0.01))
        cerebro.adddata(compose_test_data(price))
        cerebro.addsizer(bt.sizers.PercentSizer, percents=95)
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
