import unittest
from unittest import TestCase

from sympy import limit, oo, Symbol


class TestDataFrameExample(TestCase):

    def test_simple(self):
        n = Symbol('n')
        expr = 2 ** (1 - 0.5 ** n)
        a = limit(expr, n, oo)

        print(a)


if __name__ == '__main__':
    unittest.main()
