import unittest
import pandas as pd
import pyarrow as pa
import fastparquet


class ParquetFile(unittest.TestCase):
    def test_export_to_local(self):
        data = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
        data.to_parquet("test.parquet")


if __name__ == '__main__':
    unittest.main()
