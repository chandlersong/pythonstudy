import asyncio
import random
import unittest
from concurrent.futures import ProcessPoolExecutor


async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({i})...")
        await asyncio.sleep(random.randint(0,3))
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")
    return f


async def main():
    await asyncio.gather(factorial("A", 2), factorial("B", 3), factorial("C", 4), )


async def main2():
    executor = ProcessPoolExecutor(2)
    boo = asyncio.create_task(factorial("A", 5))
    baa = asyncio.create_task(factorial("B", 5))
    b = await boo
    a = await baa
    print(a, b)


class MyTestCase(unittest.TestCase):
    def test_run_as_main(self):
        asyncio.run(main())

    def test_run_as_loop(self):
        asyncio.run(main2())


if __name__ == '__main__':
    unittest.main()
