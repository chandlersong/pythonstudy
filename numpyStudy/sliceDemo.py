import unittest

import numpy as np


class SliceTestCase(unittest.TestCase):
    def test_slice_boolean(self):
        array = np.arange(9).reshape((3, 3))
        print(array)
        print(array[[True, True, False], 1])
        print(array[1, [True, True, False]])
        print(array[:, 1])
        print(array[1, :])
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
