from pyspark.sql import DataFrame


def test_app(log_data: DataFrame, check_char: str = 'a'):
    return log_data["age"].contains(check_char)
