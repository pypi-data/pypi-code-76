# -*- coding: utf-8 -*-
import time
import sched
from threading import Thread
from datetime import timedelta


def repeat(func, interval=timedelta(seconds=0), max_repeats=None):
    """
    Repeatedly invoke function at specified time interval

    Args:
        func: function to invoke

    Keyword args:
        interval (timedelta, default 0 seconds): interval to wait between each invocation
        max_repeats (integer, default None): maximum number of repeats

    Return values:
        cancel_fn (function): call this function to cancel repeat loop
    """
    cancelled = []

    def repeat(repeats_left=max_repeats or -1):
        if not cancelled and repeats_left != 0:
            try:
                func()
            except Exception as e:
                print('warning - exception encountered in backgrounded function {}'.format(func.__name__))
                print(e)
            finally:
                scheduler.enter(
                    interval.total_seconds(),
                    0,
                    lambda: repeat(repeats_left - 1),
                    []
                )

    scheduler = sched.scheduler(timefunc=time.time, delayfunc=time.sleep)
    scheduler.enter(0, 0, repeat, [])

    thread = Thread(
        target=lambda: scheduler.run()
    )
    thread.setDaemon(True)
    thread.start()

    def cancel(timeout=3):
        # putting any value in the list will cancel
        cancelled.append(None)
        thread.join(timeout)

    return cancel
