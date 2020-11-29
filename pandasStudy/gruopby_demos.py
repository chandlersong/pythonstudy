import unittest

import numpy as np
import pandas as pd


def mean_transform(x):
    return x


class GroupByCase(unittest.TestCase):
    def test_something(self):
        flags = ["a", "a", "b", "a", "b", "c", "d"]

        data = pd.DataFrame(
            {"flag": flags,
             "value": np.arange(len(flags))
             },
            index=np.arange(len(flags))
        )
        groups = data.groupby("flag")["value"].transform(mean_transform)
        print(groups)
        self.assertTrue(True)

    def test_group_by_filter(self):
        flags = ["a", "a", "b", "a", "b", "c", "d"]

        data = pd.DataFrame(
            {"flag": flags,
             "value": np.arange(len(flags))
             },
            index=np.arange(len(flags))
        )
        groups = data.groupby("flag").filter(self._group_info)
        print("============")
        print(groups)
        self.assertTrue(True)

    def _group_info(self, g):
        return g["flag"].iloc[0] == "a"


if __name__ == '__main__':
    unittest.main()
