import math

import backtrader as bt
from backtrader import Order
from loguru import logger

NO_SIGNAL = 0

CLOSE = 1

LONG = 2

SHORT = 4

CLOSE_LONG = CLOSE + LONG
CLOSE_SHORT = CLOSE + SHORT


class OrdersAbnormalAnalysis(bt.analyzers.Analyzer):

    def __init__(self):
        self.rets = []

    def notify_order(self, order):
        if order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.rets.append(
                [
                    self.data.num2date(),
                    self.strategy.broker.getposition(self.data).size,
                    self.strategy.broker.getcash(),
                    self.strategy.broker.getvalue(),
                    self.strategy._signal.signal[-1],
                    self.strategy._signal.signal[0],
                    order.created.price,
                    order.created.size,
                    order.created.value,
                    order.created.comm,

                ]
            )

    def get_analysis(self):
        return self.rets


class ExportCSVtAnalysis(bt.analyzers.Analyzer):

    def __init__(self):
        self.rets = []

    def next(self):
        self.rets.append([
            self.data.num2date(),
            self.data.open[0],
            self.data.high[0],
            self.data.low[0],
            self.data.close[0],
            self.strategy._signal.median[0],
            self.strategy._signal.upper[0],
            self.strategy._signal.lower[0],
            self.strategy._signal.signal[0],
            self.strategy.broker.getposition(self.data).size,
            self.strategy.broker.getcash(),
            self.strategy.broker.getvalue(),
        ])

    def get_analysis(self):
        return self.rets


class CrossBbands(bt.Indicator):
    lines = ('signal', 'median', 'upper', 'lower')
    params = (
        ('period', 15),
        ('bias', 1),
    )

    def __init__(self) -> None:
        logger.info(f"parameter is {self.p.period}-{self.p.bias}")

        _bbands = bt.talib.BBANDS(
            self.data,
            timeperiod=self.p.period,
            # number of non-biased standard deviations from the mean
            nbdevup=self.p.bias,
            nbdevdn=self.p.bias,
            # Moving average type: simple moving average here
            matype=0)
        self._upper = _bbands.upperband
        self._median = _bbands.middleband
        self._lower = _bbands.lowerband
        self._over_upper = bt.indicators.CrossUp(self.data, self._upper)
        self._over_lower = bt.indicators.CrossDown(self.data, self._lower)
        self._cross_median = bt.indicators.CrossOver(self.data, self._median)
        self._pre_signal = NO_SIGNAL

    def next(self):
        res = 0
        data_ = self.data.close[0]
        if self._over_upper[0]:
            upper_ = self._upper[0]
            if data_ < upper_:
                logger.error(f"error,signal is {self._upper[0]}")
            logger.debug(f"create long signal,upper is {upper_},close is {data_}")
            res = res + LONG
        if self._over_lower[0]:
            lower_ = self._lower[0]
            if data_ > lower_:
                logger.error(f"error,signal is {self._over_lower[0]}")
            logger.debug(f"create short signal,lower is {lower_},close is {data_}")
            res = res + SHORT
        if self._cross_median[0] != 0.0:
            logger.debug(
                f"ready close signal,{self._cross_median[0]},lower is {self._median[0]},close is {self.data[0]}")
            res = res + CLOSE

        if res == self._pre_signal:
            res = NO_SIGNAL
        self.lines.signal[0] = res
        self.lines.median[0] = self._median[0]
        self.lines.upper[0] = self._upper[0]
        self.lines.lower[0] = self._upper[0]


class BbandsStrategy(bt.Strategy):
    params = (
        ('period', 15),
        ('bias', 1),
    )

    def __init__(self) -> None:
        super().__init__()
        self._signal = CrossBbands(self.datas[0], period=self.p.period, bias=self.p.bias)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                logger.debug(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f,date %s' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm,
                     self.data.num2date()))
            else:  # Sell
                logger.debug('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f,date %s' %
                             (order.executed.price,
                              order.executed.value,
                              order.executed.comm,
                              self.data.num2date()))
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            logger.info(f'{self.data.num2date()},Order Canceled/Margin/Rejected')

    def next(self):

        signal = self._signal.signal[0]

        if signal == CLOSE:
            self.close()
        elif signal == LONG:
            size, price = self.cal_size_price(True)
            self.buy(size=size, price=price, exectype=Order.Limit)
        elif signal == SHORT:
            size, price = self.cal_size_price(False)
            self.sell(size=size, price=price, exectype=Order.Limit)
        elif signal == CLOSE_LONG:
            price = self.datas[0].close * (1 + 0.001)
            size = self.broker.getvalue() / price + self.broker.getposition(self.data).size
            self.buy(size=size, price=price, exectype=Order.Limit)
        elif signal == CLOSE_SHORT:
            price = self.datas[0].close * (1 - 0.001)
            size = self.broker.getvalue() / price + self.broker.getposition(self.data).size
            self.sell(size=size, price=price, exectype=Order.Limit)

    def cal_size_price(self, is_buy=True, over=0.01, cash_reduce=0.988):
        """

        :param is_buy: 是否交易
        :param over: 提高多少价格
        :param cash_reduce: 为了防止保证金过少，故意留一点
        :return:
        """
        commission_info = self.broker.getcommissioninfo(self.data).p
        if is_buy:
            price = self.datas[0].close * (1 + over)
        else:
            price = self.datas[0].close * (1 - over)
        # TODO 加入刑不行的取整逻辑
        cash = self.broker.getcash() * commission_info.leverage * (1 - commission_info.commission * 2) * cash_reduce
        size = math.floor(cash / price)
        return size, price


class StFetcher(object):
    _STRATS = []

    def __init__(self):
        logger.info(f"there are {len(self._STRATS)}")
        self._STRATS = [BbandsStrategy, BbandsStrategy]

    def __new__(cls, *args, **kwargs):
        return BbandsStrategy(*args, **kwargs)
