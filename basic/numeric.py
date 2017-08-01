import unittest
from unittest import TestCase

class TestBasicFeature(TestCase):

    def setUp(self):
        print()

    def test_mixd_type(self):
        int_double = 40+3.14

        print("int + double:{0},type:{1}".format(int_double,type(int_double)))
        print("the int will be promote to double.")

    def test_format(self):
        num = 1/3.0
        print(num)
        print("%e"%num)
        print('%4.2f'%num)
        print('{0:4.2f}'.format(num))

    def test_chain_compara(self):
        print(3>2>1) # equal to 3 > 2 and 2 >2 . but I don't suggest to use it


if __name__ == '__main__':
    unittest.main()