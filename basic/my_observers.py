import backtrader as bt


class PNLObserver(bt.Observer):
    alias = ('CashValue',)
    lines = ('pnl',)

    plotinfo = dict(plot=True, subplot=True)

    def next(self):
        position = self._owner.broker.getposition(self.data)
        self.lines.pnl[0] = position.size * (self.data.close[0] - position.price)
