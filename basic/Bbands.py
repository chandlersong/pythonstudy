import backtrader as bt
from backtrader import Order
from loguru import logger


class BbandsStrategy(bt.Strategy):
    params = (
        ('period', 15),
        ('bias', 1),
    )

    def __init__(self) -> None:
        super().__init__()
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

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                logger.debug('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f,date %s' %
                             (order.executed.price,
                              order.executed.value,
                              order.executed.comm,
                              self.data.num2date()))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            logger.debug('Order Canceled/Margin/Rejected')

        self.order = None

    def next(self):
        data_ = self.data.close[0]
        logger.debug(
            f"{self.data.num2date()},close is {data_}.upper:{self._upper[0]},lower:{self._lower[0]},midea:{self._median[0]}")
        signal = None
        if self._over_upper[0]:
            upper_ = self._upper[0]
            if data_ < upper_:
                logger.error(f"error,signal is {self._upper[0]}")
            logger.debug(f"create long signal,upper is {upper_},close is {data_}")
            size, price = self.cal_size_price(True)
            self.buy(size=size, price=price, exectype=Order.Limit)
            signal = 1
        if self._over_lower[0]:
            lower_ = self._lower[0]
            if data_ > lower_:
                logger.error(f"error,signal is {self._over_lower[0]}")
            logger.debug(f"create short signal,lower is {lower_},close is {data_}")
            size, price = self.cal_size_price(False)
            self.sell(size=size, price=price, exectype=Order.Limit)
            signal = -1
        if self._cross_median[0] != 0.0:
            self.close()
            logger.debug(
                f"ready close signal,{self._cross_median[0]},lower is {self._median[0]},close is {self.data[0]}")
            signal = 0
        logger.info(
            f",{self.data.num2date()},{self.data.open[0]},{self.data.high[0]},{self.data.low[0]},{self.data.close[0]},{self._median[0]},{self._upper[0]},{self._lower[0]},{signal}")

    def cal_size_price(self, is_buy=True, over=0.01):
        if is_buy:
            price = self.data[0] * (1 + over)
        else:
            price = self.data[0] * (1 - over)
        # TODO 加入刑不行的取整逻辑
        size = self.broker.getcash() / price
        return size, price


class StFetcher(object):
    _STRATS = []

    def __init__(self):
        logger.info(f"there are {len(self._STRATS)}")
        self._STRATS = [BbandsStrategy, BbandsStrategy]

    def __new__(cls, *args, **kwargs):
        return BbandsStrategy(*args, **kwargs)
