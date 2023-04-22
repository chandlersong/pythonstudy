import asyncio
import random

limit = asyncio.Semaphore(100)


async def _make_one_call(i):
    async with limit:
        sleep_seconds = random.randint(0, 9)
        res = f"task {i} sleep {sleep_seconds}"
        print(res)
        await asyncio.sleep(sleep_seconds)
        return res


async def make_async_call():
    tasks = [_make_one_call(i) for i in range(1000)]

    res = await asyncio.gather(*tasks)
    return res


if __name__ == '__main__':
    res = asyncio.get_event_loop().run_until_complete(make_async_call())
    print(res)
