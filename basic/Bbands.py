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

    def next(self):
        # Simply log the closing price of the series from the reference
        # logger.debug(f'{self.datas[0].datetime.datetime()}-close:{self.datas[0].close[0]}')
        logger.info(f"upper is {self._upper[0]},median is {self._median[0]},lower is {self._lower[0]}")


class StFetcher(object):
    _STRATS = []

    def __init__(self):
        logger.info(f"there are {len(self._STRATS)}")
        self._STRATS = [BbandsStrategy, BbandsStrategy]

    def __new__(cls, *args, **kwargs):
        return BbandsStrategy(*args, **kwargs)
