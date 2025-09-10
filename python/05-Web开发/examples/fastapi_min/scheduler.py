from datetime import datetime
from typing import Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger


scheduler: Optional[AsyncIOScheduler] = None


def get_scheduler() -> AsyncIOScheduler:
    global scheduler
    if scheduler is None:
        scheduler = AsyncIOScheduler()
        scheduler.start()
    return scheduler


def say_hello(name: str = "world") -> None:
    print({"time": datetime.utcnow().isoformat(), "hello": name})


def add_interval_job(seconds: int = 10, name: str = "world") -> str:
    sch = get_scheduler()
    job = sch.add_job(say_hello, IntervalTrigger(seconds=seconds), kwargs={"name": name})
    return job.id

def list_jobs() -> list[dict[str, str]]:
    sch = get_scheduler()
    return [{"id": j.id, "next_run_time": str(j.next_run_time)} for j in sch.get_jobs()]


