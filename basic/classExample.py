import unittest
from unittest import TestCase

class Base:
    pass

class Derived(Base):
    pass

class TestIsInstance(TestCase):

    def test_is_instance(self):
        parent = Base()
        child = Derived()

        self.assertTrue(isinstance(parent,Base))
        self.assertTrue(isinstance(child,Base))
        self.assertFalse(isinstance(parent,Derived))
        self.assertTrue(isinstance(child,Derived))


if __name__ == '__main__':
    unittest.main()