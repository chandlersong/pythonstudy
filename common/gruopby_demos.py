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

    def test_find_max(self):
        data = pd.read_csv("data1.csv", parse_dates=['candle_begin_time'], index_col=['candle_begin_time'])
        del data["AtrVolatility_[3, 9, 0.3]"]
        data.columns = ["symbol", "v1", "v2"]
        x = data[data["v2"] > 0.5]
        x.to_csv("middle.csv")
        x = x.groupby("candle_begin_time").agg({'symbol': 'first', 'v1': 'max'})
        x["tag"] = 1
        print(x)
        new_df = pd.merge(data, x, how='left', left_on=["candle_begin_time", 'symbol'],
                          right_on=["candle_begin_time", 'symbol'], suffixes=('', '_DROP')).filter(regex='^(?!.*_DROP)')
        print(new_df.to_csv("bb.csv"))

    def _group_info(self, g):
        return g["flag"].iloc[0] == "a"


if __name__ == '__main__':
    unittest.main()
