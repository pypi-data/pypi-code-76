import string
import random 

import os 
import sys 

__version__ = 0.1


def nitro(t="c"):
    if t == "c":
        gentype = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
        c = "https://discord.gift/"
        for x in range(16):
            p = random.choice(gentype)
            c += p 
        return c 
    if t == "b":
        gentype = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
        c = "https://discord.gift/"
        for x in range(24):
            p = random.choice(gentype)
            c += p 
        return c 
    else:
        return "ERROR: Only 'nitro('c')' or 'nitro('b')' is accepted."
