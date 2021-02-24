import subprocess

from .module import Module


class Interfaces(Module):

    def __str__(self):
        ints = subprocess.Popen(['ip', '-4', '-h', '-o', '-c', '-br', 'a'], stdout=subprocess.PIPE)
        ints = subprocess.Popen(['awk', '{print $1,$2,$3}'], stdin=ints.stdout, stdout=subprocess.PIPE)
        return(ints.stdout.read().decode())
