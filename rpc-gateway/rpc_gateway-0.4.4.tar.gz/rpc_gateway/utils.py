from typing import Optional, Awaitable, Any
import asyncio


def await_sync(awaitable: Awaitable, loop: Optional[asyncio.AbstractEventLoop] = None, timeout: Optional[float] = None) -> Any:
    loop = loop or asyncio.get_event_loop()
    if loop.is_running():
        future = asyncio.run_coroutine_threadsafe(awaitable, loop or asyncio.get_event_loop())
        return future.result(timeout=timeout)
    else:
        try:
            return loop.run_until_complete(awaitable)
        except asyncio.CancelledError:
            pass
