import asyncio
import random
import time

from loguru import logger

limit = asyncio.Semaphore(100)


async def _make_one_call(i):
    async with limit:
        sleep_seconds = random.randint(2, 9)
        loop = asyncio.get_running_loop()
        logger.info(f"task {i} will be submit")
        await loop.run_in_executor(None, time.sleep, sleep_seconds)

        logger_text = f"task {i} sleep {sleep_seconds}"
        logger.info(logger_text)
        return logger_text


async def make_async_call():
    tasks = [_make_one_call(i) for i in range(1000)]

    res = await asyncio.gather(*tasks)
    return res


if __name__ == '__main__':
    print_text = asyncio.get_event_loop().run_until_complete(make_async_call())
    print(print_text)
