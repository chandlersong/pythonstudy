import random
import string
from typing import List

from pyspark.sql import DataFrame


def test_app(log_data: DataFrame, check_char: str = 'a'):
    return log_data["age"].contains(check_char)


def create_random_data(row_num: int) -> List[tuple]:
    result = list()
    a_str = string.ascii_uppercase
    for i in range(row_num):
        random_letter = random.choice(a_str)
        result.append((random_letter, random.randint(1, row_num), random.random()))
    return result
