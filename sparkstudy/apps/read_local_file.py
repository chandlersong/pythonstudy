from pyspark.sql import DataFrame

from sparkstudy.deploy.demo_sessions import DemoSQLSessionFactory


def test_app(log_data: DataFrame, check_char: str = 'a'):
    return log_data.value.contains(check_char)


if __name__ == '__main__':
    logFile = "../../data/people.csv"  # Should be some file on your system
    sessionFactory = DemoSQLSessionFactory(name="local file")
    spark = sessionFactory.build_session()
    logData = spark.read.text(logFile).cache()

    numAs = logData.filter(test_app(logData, "a")).count()
    numBs = logData.filter(logData.value.contains('b')).count()

    print("Lines with a: %i, lines with b: %i" % (numAs, numBs))

    spark.stop()
