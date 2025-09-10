import asyncio
from contextlib import asynccontextmanager


@asynccontextmanager
async def limited(semaphore: asyncio.Semaphore):
    await semaphore.acquire()
    try:
        yield
    finally:
        semaphore.release()


async def worker(task_id: int, semaphore: asyncio.Semaphore) -> str:
    async with limited(semaphore):
        await asyncio.sleep(0.1)
        return f"done-{task_id}"


async def main() -> None:
    semaphore = asyncio.Semaphore(3)
    tasks = [asyncio.create_task(worker(i, semaphore)) for i in range(10)]
    try:
        results = await asyncio.gather(*tasks)
        print(results)
    except asyncio.CancelledError:
        for t in tasks:
            t.cancel()
        raise


if __name__ == "__main__":
    asyncio.run(main())
