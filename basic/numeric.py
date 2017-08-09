import unittest
from unittest import TestCase

import decimal
from decimal import Decimal

class TestBasicFeature(TestCase):
    def setUp(self):
        print()

    def test_mixd_type(self):
        int_double = 40 + 3.14

        print("int + double:{0},type:{1}".format(int_double, type(int_double)))
        print("the int will be promote to double.")

    def test_format(self):
        num = 1 / 3.0
        print(num)
        print("%e" % num)
        print('%4.2f' % num)
        print('{0:4.2f}'.format(num))

    def test_chain_compara(self):
        print(3 > 2 > 1)  # equal to 3 > 2 and 2 >2 . but I don't suggest to use it

    def test_division(self):
        X = 5
        Y = 2
        print("X/Y:{0}".format(X / Y))  # 真实数据
        print("X//Y:{0}".format(X // Y))  # 求倍数

        print("6/float(2):{0}".format(6 / float(2)))

    def test_complex_number(self):
        print("1j*1J:{0}".format(1j * 1J))

    def test_hex_otc_bin(self):
        number = 64
        print("hex:{0},otc:{1},bin:{0},".format(oct(number),hex(number),bin(number)))


class DecimalTest(TestCase):

    def test_basic_feature(self):
        print(Decimal('0.1') + Decimal('0.1') + Decimal('0.1') - Decimal('0.3'))

    def test_set_global_precision(self):
        print("before set precision")
        print(decimal.Decimal(1) / decimal.Decimal(7))
        decimal.getcontext().prec = 5
        print("after set precision")
        print(decimal.Decimal(1) / decimal.Decimal(7))



if __name__ == '__main__':
    unittest.main()
