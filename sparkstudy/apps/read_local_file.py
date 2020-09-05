from pyspark import SparkConf
from pyspark.sql import SparkSession, DataFrame


def test_app(log_data: DataFrame, check_char: str = 'a'):
    return log_data.value.contains(check_char)


if __name__ == '__main__':
    logFile = "../../resource/people.csv"  # Should be some file on your system
    conf = SparkConf().setMaster("local[3]").setAppName("MY First App")
    spark = SparkSession.builder.config(conf=conf).getOrCreate()
    logData = spark.read.text(logFile).cache()

    numAs = logData.filter(test_app(logData, "a")).count()
    numBs = logData.filter(logData.value.contains('b')).count()

    print("Lines with a: %i, lines with b: %i" % (numAs, numBs))

    spark.stop()
