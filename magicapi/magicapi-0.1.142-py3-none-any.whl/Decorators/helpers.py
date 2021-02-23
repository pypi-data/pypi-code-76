import inspect


async def async_safe(f, *args, **kwargs):
    if inspect.iscoroutinefunction(f):
        return await f(*args, **kwargs)
    return f(*args, **kwargs)
