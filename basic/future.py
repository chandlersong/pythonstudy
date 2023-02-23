class CalculateCloseOut:

    def __init__(self):
        self._min_margin_ratio = 0.005
        self._c_rate = 0.0001

    def __call__(self, cash, position, open_price, is_long):
        direction = -1
        if is_long:
            direction = 1
        return (cash - position * open_price * direction) / (
                position * (self._min_margin_ratio + self._c_rate - direction))
