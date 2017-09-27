import pstats
import unittest
from unittest import TestCase
import cProfile
import timeit
import re
import io
import timeit

def method_profile():
    1 + 1

# https://docs.python.org/2/library/timeit.html
# cProfile.run('re.compile("foo|bar")')

print(timeit.timeit('"-".join(str(n) for n in range(100))', number=10000))