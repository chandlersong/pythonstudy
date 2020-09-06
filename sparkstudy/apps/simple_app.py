from sparkstudy.deploy.demo_sessions import DemoSQLSessionFactory
from sparkstudy.libs.tools import test_app

if __name__ == '__main__':
    sessionFactory = DemoSQLSessionFactory(remote=True)
    spark = sessionFactory.build_session()
    spark.sparkContext.setLogLevel("ERROR")
    logData = spark.createDataFrame(["aaabbbb", "bbfbfb", "aaaaaaa"], "string").toDF("age").cache()

    numAs = logData.filter(test_app(logData, 'a')).count()
    numBs = logData.filter(logData["age"].contains('b')).count()

    print("Lines with a: %i, lines with b: %i" % (numAs, numBs))

    spark.stop()
