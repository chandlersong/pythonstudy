import unittest

from loguru import logger

from basic.future import CalculateCloseOut


class CalculateCloseOutTestCase(unittest.TestCase):
    def test_long(self):
        closeout_calculate = CalculateCloseOut()
        position = 100
        open_price = 10
        leverage = 5
        cash = position * open_price / leverage

        closeout_price = closeout_calculate(cash, position, open_price, True)
        print(closeout_price)
        logger.info(f"cash is {cash},buy {position},open price is {open_price}")
        profit = position * (closeout_price - open_price)
        logger.info(f"close out price is {closeout_price},profit is {profit}")
        self.assertEqual(8.041009146647905, closeout_price)

    def test_short(self):
        closeout_calculate = CalculateCloseOut()
        position = 100
        open_price = 10
        leverage = 5
        cash = position * open_price / leverage

        closeout_price = closeout_calculate(cash, position, open_price, False)
        print(closeout_price)
        logger.info(f"cash is {cash},buy {position},open price is {open_price}")
        profit = position * (closeout_price - open_price)
        logger.info(f"close out price is {closeout_price},profit is {profit}")
        self.assertEqual(11.939110536265048, closeout_price)


if __name__ == '__main__':
    unittest.main()
