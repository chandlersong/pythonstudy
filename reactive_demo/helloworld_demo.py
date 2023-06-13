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

    def test_mulit_subscribe(self):
        """
        一次subscribe。pip会跑一次
        :return:
        """
        source = rx.of("Alpha", "Beta", "Gamma", "Delta", "Epsilon")

        composed = source.pipe(
            ops.do_action(lambda s: print(f"pip+{s}")),
            ops.map(lambda s: len(s)),
            ops.filter(lambda i: i >= 5)
        )
        composed.subscribe(lambda value: print("1st Received {0}".format(value)))
        composed.subscribe(lambda value: print("2nd Received {0}".format(value)))
        print("ok")

    def test_interval(self):
        """
        这个方法，主要是介绍了一下子基建事情
        1. 用了run，会不停的处理
           1. 如何在pipe中中断相应的操作。take_while
        2. do action的类似于java中的peek
        3. timer
        :return:
        """
        start = time.time()

        def print_value(value):
            print("Next: {} \t({} ms)".format(value, millis_since(start)))
            if value > 5:
                return None
            else:
                return value

        def do_wile(value):
            print("do while: {})".format(value))
            return value is not None

        source = rx.timer(0, period=0.5).pipe(
            ops.map(print_value),
            ops.take_while(do_wile)
        )

        source.run()


if __name__ == '__main__':
    unittest.main()
