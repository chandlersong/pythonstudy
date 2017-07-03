import unittest
from unittest import TestCase

from pyalgotrade import dataseries
from pyalgotrade.technical.cumret import CumulativeReturn


class TestBuildIn(TestCase):
    def test_cumulativeReturn(self):
        seqDS = dataseries.SequenceDataSeries()
        cumulativeReturn = CumulativeReturn(seqDS)

        for i in range(1, 51):
            seqDS.append(i)
            print(cumulativeReturn[i-1])

    def test_line(self):
        seqDS = dataseries.SequenceDataSeries()
        cumulativeReturn = CumulativeReturn(seqDS)

        for i in range(1, 51):
            seqDS.append(i)
            print(cumulativeReturn[i - 1])



if __name__ == '__main__':
    unittest.main()