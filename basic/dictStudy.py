import unittest
from unittest import TestCase

class DictTest(TestCase):
    def test_create_dict(self):
        rec = {'name': {'first': 'Bob', 'last': 'Smith'},
               'jobs': ['dev', 'mgr'],
               'age': 40.5}
        print(rec)

if __name__ == '__main__':
    unittest.main()