import builtins
import random
import sys

EMOS = open("emolist.txt", "r").read()

def print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False):
    builtins.print(*objects, random.choice(EMOS))