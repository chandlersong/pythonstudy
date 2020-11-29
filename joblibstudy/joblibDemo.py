import unittest
from math import sqrt

import numpy as np

from joblib import Memory, Parallel, delayed


class MemoryCase(unittest.TestCase):
    def test_hello_world_of_memory(self):
        cache_dir = 'cache'
        mem = Memory(cache_dir)
        a = np.vander(np.arange(3)).astype(np.float)
        square = mem.cache(np.square)
        b = square(a)
        print(b)

        c = square(a)
        print(c)


def my_function(i):
    print(i)
    return sqrt(i)


class ParallelCase(unittest.TestCase):
    def test_hello_world_of_parallel(self):
        Parallel(n_jobs=3)(delayed(my_function)(i ** 2) for i in range(10))


if __name__ == '__main__':
    unittest.main()
