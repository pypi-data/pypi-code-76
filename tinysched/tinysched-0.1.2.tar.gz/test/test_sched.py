import unittest
import time
from datetime import timedelta

from tinysched import scheduler


class TestSched(unittest.TestCase):
    def setUp(self):
        self.count = 0

    def test_repeat(self):
        repeats = 3
        scheduler.repeat(self.inc_counter, timedelta(seconds=0), max_repeats=repeats)
        time.sleep(0.1)
        self.assertEqual(self.count, repeats)

    def test_interval(self):
        repeats = 3
        delay = 0.01
        scheduler.repeat(self.inc_counter, timedelta(seconds=delay), max_repeats=repeats)
        for r in range(repeats):
            self.assertLessEqual(self.count, r + 1)
            time.sleep(delay)

    def test_exception_recovery(self):
        repeats = 3

        def foo():
            self.count += 1
            raise RuntimeError('foo!')

        scheduler.repeat(foo, timedelta(seconds=0), max_repeats=repeats)
        time.sleep(0.1)
        self.assertEqual(self.count, repeats)

    def inc_counter(self):
        self.count += 1
