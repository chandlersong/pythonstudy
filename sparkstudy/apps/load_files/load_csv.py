import os

from pyspark.sql.column import StringType
from pyspark.sql.functions import input_file_name, udf
from pyspark.sql.types import StructType, DoubleType, StructField

from sparkstudy.deploy import find_root
from sparkstudy.deploy.demo_sessions import DemoSQLSessionFactory


def calculate_tag(path: str) -> str:
    result = path.split("/")[-1]
    return result


tags_define_column = udf(calculate_tag, StringType())

if __name__ == '__main__':
    sessionFactory = DemoSQLSessionFactory(name="local csv")
    spark = sessionFactory.build_session()
    workspace = find_root()
    df = spark.read.csv(os.path.join(workspace, "resource", "assertReport"), header="true",
                        inferSchema=True).withColumn(
        "tag", tags_define_column(input_file_name()))

    print(df.dtypes)
    df.show()

    df = df.rdd.keyBy(lambda row: row["tag"])
    # df.foreach(lambda key: print(key[0]))

    print(type(df))
