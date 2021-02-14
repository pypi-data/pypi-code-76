try:
    from apscheduler.schedulers.asyncio import AsyncIOScheduler  # type: ignore
except ImportError:
    # APScheduler is not installed
    AsyncIOScheduler = None

if AsyncIOScheduler:

    class Scheduler(AsyncIOScheduler):
        pass


else:
    Scheduler = None  # type: ignore


__all__ = [
    "Scheduler",
]
