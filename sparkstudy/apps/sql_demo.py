import unittest

from sparkstudy.deploy.demo_sessions import DemoSQLSessionFactory


class SQLDemos(unittest.TestCase):

    def setUp(self) -> None:
        self.session_factory = DemoSQLSessionFactory(name="sql relative")

    def test_join(self):
        """
        doesn't support join on view?
        :return:
        """
        spark = self.session_factory.build_session()
        df = spark.createDataFrame([
            (2.2, True, "1", "foo"),
            (3.3, False, "2", "bar"),
            (4.4, False, "3", "baz"),
            (5.5, False, "4", "foo")
        ], ["real", "bool", "stringNum", "string"])
        df.createTempView("view1")
        df1 = spark.createDataFrame([
            ("1"),
            ("2"),
            ("3"),
            ("4")
        ], ["fake"])
        df1.createTempView("view2")

        df_join = spark.sql("select view1.real from view1 join view2 on view1.stringNum = view2.fake")
        print(df_join.show())


if __name__ == '__main__':
    unittest.main()
