from .runner import DayRunner, HourRunner


def hourly(func, timer):
    HourRunner(func, timer)

def daily(func, timer):
    DayRunner(func, timer)
