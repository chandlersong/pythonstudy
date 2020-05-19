import unittest
from functools import wraps


class AnnotationTestCase(unittest.TestCase):
    def test_simple(self):
        do_something()
        self.assertEqual(True, True)

    def test_functools_wrapper(self):
        do_wrapper()
        self.assertEqual(True, True)

    def test_arguments(self):
        with_argument()
        self.assertEqual(True, True)


def do_annotation(fn):
    return fn


@do_annotation
def do_something():
    print("do something")


def annotation_wrap(fn):
    @wraps(fn)
    def wrapper(*args, **kwds):
        print("in wrapper")
        return fn(*args, **kwds)

    return wrapper


@annotation_wrap
def do_wrapper():
    print("do wrapper")


def decorator_with_argument(ok):
    def decorator(fn):
        print("in decorater")

        def wrapper(*args, **kwargs):
            print("in wrapper")
            print(ok)
            result = fn(*args, **kwargs)
            return result

        return wrapper

    return decorator


@decorator_with_argument(ok="ok")
def with_argument():
    print("with_argument")


if __name__ == '__main__':
    unittest.main()
