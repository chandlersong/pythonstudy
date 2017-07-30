import unittest
from unittest import TestCase


class DictTest(TestCase):
    def test_create_dict(self):
        rec = {'name': {'first': 'Bob', 'last': 'Smith'},
               'jobs': ['dev', 'mgr'],
               'age': 40.5}
        print(rec)

    def test_intersection(self):
        X = set('spam')
        Y = {'h', 'a', 'm'}

        print("Intersection"+str(X & Y))
        print("Union"+str(X | Y))
        print("Difference" + str(X - Y))
        print("Superset:" + str( X > Y)) #超集

if __name__ == '__main__':
    unittest.main()
