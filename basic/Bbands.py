from backtrader import Strategy
from loguru import logger


class BbandsStrategy(Strategy):
    def next(self):
        # Simply log the closing price of the series from the reference
        # logger.debug(f'{self.datas[0].datetime.datetime()}-close:{self.datas[0].close[0]}')
        pass


class StFetcher(object):
    _STRATS = [BbandsStrategy, BbandsStrategy]

    def __new__(self, *args, **kwargs):
        logger.info(f"**kwargs is {kwargs}")
        idx = kwargs.pop('idx')
        logger.info(f"idx is {idx},{len(self._STRATS)}")
        obj = self._STRATS[idx](*args, **kwargs)
        logger.info(f"obj is {obj}")
        return obj
