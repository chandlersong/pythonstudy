import os

from pyspark.sql.column import StringType
from pyspark.sql.functions import input_file_name, udf
from pyspark.sql.types import StructType, DoubleType, StructField

from sparkstudy.deploy import find_root
from sparkstudy.deploy.demo_sessions import DemoSQLSessionFactory


def calculate_tag(path: str) -> str:
    result = path.split("/")[-1]
    return result


"""
custom column of spark
"""
tags_define_column = udf(calculate_tag, StringType())

if __name__ == '__main__':
    sessionFactory = DemoSQLSessionFactory(name="local csv")
    spark = sessionFactory.build_session()
    workspace = find_root()
    """
    Be careful!!! header="true" not use True
    """
    df = spark.read.csv(os.path.join(workspace, "resource", "assertReport"), header="true",
                        inferSchema=True).withColumn(
        "tag", tags_define_column(input_file_name()))

    print("default partitions {}".format(df.rdd.getNumPartitions()))
    df = df.repartition(300, "报告日期")

    print(df.explain())
    """
    the partition is automatically. if you want use handle. use method in rdd
    """
    print("partitions by 报告日期 {}".format(df.rdd.getNumPartitions()))
    """
    parquet don't have header in file
    """
    df.write.option("header", "true").parquet("data", mode="overwrite")
