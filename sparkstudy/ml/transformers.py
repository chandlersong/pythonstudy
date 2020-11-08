from pyspark.ml import Transformer
from pyspark.sql import DataFrame
from pyspark.sql.functions import length


class DemoTransformer(Transformer):
    """
    A custom Transformer which drops all columns that have at least one of the
    words from the banned_list in the name.
    """

    def __init__(self):
        super(DemoTransformer, self).__init__()

    def _transform(self, df: DataFrame) -> DataFrame:
        return df.withColumn('new', length('text'))
