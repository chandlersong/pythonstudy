from pyspark.sql import SparkSession

from sparkstudy.libs.tools import test_app

logFile = "YOUR_SPARK_HOME/README.md"  # Should be some file on your system
spark = SparkSession.builder.appName("SimpleApp").getOrCreate()
logData = spark.createDataFrame(["aaabbbb", "bbfbfb", "aaaaaaa"], "string").toDF("age").cache()

numAs = logData.filter(test_app(logData, 'a')).count()
numBs = logData.filter(logData["age"].contains('b')).count()

print("Lines with a: %i, lines with b: %i" % (numAs, numBs))

spark.stop()
