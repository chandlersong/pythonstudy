import backtrader as bt
from loguru import logger


class BbandsStrategy(bt.Strategy):
    params = (
        ('period', 15),
    )

    def __init__(self) -> None:
        super().__init__()
        logger.info(f"parameter is {self.p.period}")
        self.sma = bt.talib.SMA(self.data, timeperiod=self.p.period)

    def next(self):
        # Simply log the closing price of the series from the reference
        # logger.debug(f'{self.datas[0].datetime.datetime()}-close:{self.datas[0].close[0]}')
        pass


class StFetcher(object):
    _STRATS = []

    def __init__(self):
        logger.info(f"there are {len(self._STRATS)}")
        self._STRATS = [BbandsStrategy, BbandsStrategy]

    def __new__(cls, *args, **kwargs):
        return BbandsStrategy(*args, **kwargs)
