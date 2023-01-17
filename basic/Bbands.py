from backtrader import Strategy


class BbandsStrategy(Strategy):
    def next(self):
        # Simply log the closing price of the series from the reference
        # logger.debug(f'{self.datas[0].datetime.datetime()}-close:{self.datas[0].close[0]}')
        pass