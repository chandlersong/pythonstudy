import os
import unittest
from unittest import TestCase

from pyspark.sql.column import StringType
from pyspark.sql.functions import input_file_name, udf

from sparkstudy.deploy import find_root
from sparkstudy.deploy.demo_sessions import DemoSQLSessionFactory


def calculate_tag(path: str) -> str:
    result = path.split("/")[-1]
    return result


"""
custom column of spark
"""
tags_define_column = udf(calculate_tag, StringType())


def partition_by_key(row) -> int:
    return hash(row)


class DataFrameDemos(TestCase):

    def setUp(self) -> None:
        """
           Be careful!!! header="true" not use True
        """
        workspace = find_root()
        session_factory = DemoSQLSessionFactory(name="local csv")
        spark = session_factory.build_session()
        self.df = spark.read.csv(os.path.join(workspace, "resource", "assertReport"), header="true",
                                 inferSchema=True).withColumn(
            "tag", tags_define_column(input_file_name()))

    def test_partition_by_func(self):
        rdd_df = self.df.rdd.map(lambda el: (el["tag"], el)).partitionBy(3, partitionFunc=partition_by_key).persist()
        print("Number of partitions: {}".format(rdd_df.getNumPartitions()))
        print("Partitioner: {}".format(rdd_df.partitioner))
        print("type of rdd:{}".format(type(rdd_df)))

        rdd_df.toDF().foreach(lambda row: print(row))

    def test_write_to_local(self):
        self.df.write.option("header", "true").parquet("data", mode="overwrite")

    def test_partition_info(self):
        df = self.df
        print("default partitions {}".format(df.rdd.getNumPartitions()))
        df = df.repartition(300, "报告日期")

        print(df.explain())

        """
           the partition is automatically. if you want use handle. use method in rdd
        """
        print("partitions by 报告日期 {}".format(df.rdd.getNumPartitions()))

    def test_df_pick_column(self):
        df = self.df
        print(df.select("tag").distinct().show())


if __name__ == '__main__':
    unittest.main()
