import unittest
from pyhive import hive


class MyTestCase(unittest.TestCase):
    def test_create_conntection(self):
        with hive.Connection(host='192.168.64.23', port=30085) as conn:
            cursor = conn.cursor()
            cursor.execute('select * from pokes limit 10')
            for result in cursor.fetchall():
                print(result)


if __name__ == '__main__':
    unittest.main()
