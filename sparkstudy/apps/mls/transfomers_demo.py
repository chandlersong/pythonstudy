import unittest
from pyspark.ml.feature import HashingTF, IDF, Tokenizer

from sparkstudy.deploy.demo_sessions import DemoSQLSessionFactory


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.session_factory = DemoSQLSessionFactory(name="sql relative")

    def test_hello_world(self):
        spark = self.session_factory.build_session()

        sentence_data = spark.createDataFrame([
            (0.0, "Hi I heard about Spark"),
            (0.0, "I wish Java could use case classes"),
            (1.0, "Logistic regression models are neat")
        ], ["label", "sentence"])

        tokenizer = Tokenizer(inputCol="sentence", outputCol="words")
        words_data = tokenizer.transform(sentence_data)

        print(words_data.show())

        hashing_tf = HashingTF(inputCol="words", outputCol="rawFeatures", numFeatures=20)
        featurized_data = hashing_tf.transform(words_data)
        # alternatively, CountVectorizer can also be used to get term frequency vectors

        idf = IDF(inputCol="rawFeatures", outputCol="features")
        idf_model = idf.fit(featurized_data)
        rescaled_data = idf_model.transform(featurized_data)

        print(rescaled_data.select("label", "features").show())


if __name__ == '__main__':
    unittest.main()
