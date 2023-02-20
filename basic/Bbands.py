import backtrader as bt
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

    def next(self):
        data_ = self.data[0]
        if self._over_upper[0]:
            upper_ = self._upper[0]
            if data_ < upper_:
                logger.error(f"error,signal is {self._upper[0]}")
            logger.debug(f"create long signal,upper is {upper_},close is {data_}")
        if self._over_lower[0]:
            lower_ = self._lower[0]
            if data_ > lower_:
                logger.error(f"error,signal is {self._over_lower[0]}")
            logger.debug(f"create short signal,lower is {lower_},close is {data_}")
        if self._cross_median[0] != 0.0:
            logger.debug(
                f"ready close signal,{self._cross_median[0]},lower is {self._median[0]},close is {self.data[0]}")


class StFetcher(object):
    _STRATS = []

    def __init__(self):
        logger.info(f"there are {len(self._STRATS)}")
        self._STRATS = [BbandsStrategy, BbandsStrategy]

    def __new__(cls, *args, **kwargs):
        return BbandsStrategy(*args, **kwargs)
