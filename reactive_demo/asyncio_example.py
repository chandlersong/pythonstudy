import asyncio
import functools
import reactivex as rx
from reactivex.scheduler.eventloop import AsyncIOScheduler
from reactivex.disposable import Disposable

if __name__ == '__main__':
    def from_aiter(iter, loop):
        def on_subscribe(observer, scheduler):
            async def _aio_sub():
                try:
                    async for i in iter:
                        observer.on_next(i)
                    loop.call_soon(
                        observer.on_completed)
                except Exception as e:
                    loop.call_soon(
                        functools.partial(observer.on_error, e))

            task = asyncio.ensure_future(_aio_sub(), loop=loop)
            return Disposable(lambda: task.cancel())

        return rx.create(on_subscribe)


    async def ticker(delay, to):
        """Yield numbers from 0 to `to` every `delay` seconds."""
        for i in range(to):
            yield i
            await asyncio.sleep(delay)


    async def main(loop):
        finish_event = asyncio.Event()

        def on_completed():
            print("completed")
            finish_event.set()

        disposable = from_aiter(ticker(1, 10), loop).subscribe(
            on_next=lambda i: print("next: {}".format(i)),
            on_error=lambda e: print("error: {}".format(e)),
            on_completed=on_completed,
        )

        await finish_event.wait()
        disposable.dispose()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))