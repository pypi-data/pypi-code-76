from time import*
from sys import*

def clean(a):
    sleep(a)
    stdout.write('\033[2J\033[00H')
def clear():
    stdout.write('\033[2J\033[00H')