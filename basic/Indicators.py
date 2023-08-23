import backtrader as bt


class ProfitIndicator(bt.Indicator):
    lines = ('pnl',)
    params = (('broker', None),)


    def next(self):
        position = self.p.broker.getposition(self.data)
        self.lines.pnl[0] = position.size * (self.data.close[0] - position.price)
