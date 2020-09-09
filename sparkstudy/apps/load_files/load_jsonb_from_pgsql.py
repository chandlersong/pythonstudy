import json

from sparkstudy.deploy import find_root
from sparkstudy.deploy.demo_sessions import DemoSQLSessionFactory

if __name__ == '__main__':
    sessionFactory = DemoSQLSessionFactory(name="local csv")
    spark = sessionFactory.build_session()
    workspace = find_root()

    df1 = spark.read.jdbc("jdbc:postgresql://172.168.0.1:5432/postgres?user=postgres&password=password", "spark_json")

    print(df1.show())
    print(df1.dtypes)
