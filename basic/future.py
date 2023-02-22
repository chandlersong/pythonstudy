
class CalculateCloseOut:

    def __init__(self):
        self.__min_margin_ratio = 0.005
        self._c_rate = 0.0001

    def __call__(self, *args, **kwargs):
        temp = self._c_rate + self.__min_margin_ratio

        pass
