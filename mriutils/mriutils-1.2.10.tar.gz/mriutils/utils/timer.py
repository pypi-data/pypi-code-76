#!/usr/bin/env python

import time

class Timer():
    def __init__(self):
        self.start_time = self.start()
        self.end_time = 0
        self.interval = 0

    def start(self):
        self.time = time.time()
        self.end_time = 0
        self.interval = 0

    def end(self):
        self.end_time = time.time()
        self.interval = self.end_time - self.start_time
        return self.interval
