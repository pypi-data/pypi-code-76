from collections import namedtuple
from subprocess import Popen, PIPE


class Base:
    fields = None

    def tmux(self, cmd, *args, format=None, target=None):
        cmd = 'tmux', cmd
        if args:
            cmd+=args
        if format:
            cmd+=('-F', format)
        if target:
            cmd+=('-t', target)

        try:
            proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
            stdout, stderr = proc.communicate()
            ret = proc.returncode
        except Exception as x:
            print(f'\n ! {" ".join(cmd)} \n ! {x}\n')
            raise RuntimeError

        err = stderr.decode().strip()
        if err:
            print(f'\n ! {" ".join(cmd)} [{ret}]\n ! {err}\n')
            raise RuntimeError

        lines = [line.strip() for line in stdout.decode().split('\n') if line.strip()]

        return lines

    def __getattr__(self, name):
        val = getattr(self.fields, name, None)
        if val is None:
            val = getattr(self.active, name)
        return val

    @classmethod
    def spec(cls):
        if not hasattr(cls, 'nt'):
            keys = [
                k.strip()
                for k in cls.Child.keys.split()
                if k.strip()
            ]
            cls.nt = namedtuple('fields', keys)
        return cls.nt._fields, cls.nt._make

    def format(self, keys):
        fl = ['#{%s}' % k for k in keys]
        sep = '\t'
        return sep.join(fl)

    @property
    def children(self):
        keys, make = self.spec()
        if isinstance(self.list_cmd, tuple):
            cmd, arg = self.list_cmd
            lines = self.tmux(
                cmd, arg,
                format = self.format(keys),
            )
        else:
            lines = self.tmux(
                self.list_cmd,
                format = self.format(keys),
            )
        for line in lines:
            vals = line.split('\t')
            fields = make(vals)
            yield self.Child(self, fields)

    @property
    def is_active(self):
        isactive = f'{self.__class__.__name__.lower()}_active'
        return getattr(self, isactive)=='1'

    @property
    def active(self):
        for child in self.children:
            if child.is_active:
                return child
