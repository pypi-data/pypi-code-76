from .runner import DayRunner, HourRunner


def hourly(func, timer, run_on_init=True):
    HourRunner(func, timer, run_on_init)

def daily(func, timer, run_on_init=True):
    DayRunner(func, timer, run_on_init)
