from concurrent.futures import ThreadPoolExecutor

from typing import Any

executor = ThreadPoolExecutor(max_workers=500)


def execute_func_in_individual_thread(func: Any, ex: ThreadPoolExecutor = executor, **kwargs, ):
    task = ex.submit(func, **kwargs)
    # ex.shutdown()
    return task
