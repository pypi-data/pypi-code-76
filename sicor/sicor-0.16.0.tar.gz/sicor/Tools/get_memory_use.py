import os
import psutil

__author__ = 'Niklas Bohn, Andre Hollstein'


def get_memory_use():
    return psutil.Process(os.getpid()).memory_info()[0] / float(2 ** 20)
