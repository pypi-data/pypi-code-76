import subprocess

from .module import Module


class Resolve(Module):
    
    def __str__(self):
        _proc = subprocess.Popen(['systemd-resolve', '--status'], stdout=subprocess.PIPE)
        _proc = subprocess.Popen(['grep', 'DNS Server\|Link\|Global'], stdin=_proc.stdout, stdout=subprocess.PIPE)

        return(_proc.stdout.read().decode())
