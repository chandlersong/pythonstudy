import time
import unittest

import reactivex as rx
from reactivex import operators as ops


def millis_since(t0):
    return int((time.time() - t0) * 1000)



class MyTestCase(unittest.TestCase):
    def test_something(self):
        source = rx.of("Alpha", "Beta", "Gamma", "Delta", "Epsilon")

        composed = source.pipe(
            ops.map(lambda s: len(s)),
            ops.filter(lambda i: i >= 5)
        )
        composed.subscribe(lambda value: print("Received {0}".format(value)))
        print("ok")

    def test_interval(self):
        """
        这个方法，主要是介绍了一下子基建事情
        1. 用了run，会不停的处理
        2. do action的类似于java中的peek
        3. timer
        :return:
        """
        start = time.time()

        def print_value(value):
            print("Next: {} \t({} ms)".format(value, millis_since(start)))

        source = rx.timer(0, period=2).pipe(
            ops.do_action(print_value)
        )

        subscription = source.run()



if __name__ == '__main__':
    unittest.main()
