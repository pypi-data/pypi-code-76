from re import search
from time import sleep
from types import SimpleNamespace as ns

from .base import Base


class Pane(Base):
    keys = '''
        session_id
        window_id
        pane_id
        pane_active
        pane_index
        pane_width
        pane_height
        pane_title
        pane_pid
        pane_start_command
        pane_start_path
        pane_current_path
        pane_current_command
    '''

    def __init__(self, window, fields):
        self.window = window
        self.fields = fields

    def send(self, keys):
        self.tmux('send-keys', keys)
        self.tmux('send-keys', 'Enter')

    def send_keys(self, keys):
        self.tmux('send-keys', keys)

    def zoom(self):
        self.tmux('resize-pane', '-Z')

    @property
    def width(self):
        return int(self.pane_width)

    @width.setter
    def width(self, percent):
        w = self.window.width
        val = int(w*percent/100)
        self.tmux('resize-pane', f'-x{val}')

    @property
    def capture(self):
        return self.tmux('capture-pane', '-p')

    def search(self, pat, line, num):
        found = search(pat, line)
        if found:
            grp = found.groupdict()
            grp['line'] = line
            grp['num'] = num
            return ns(**grp)

    def parse(self, pat, num=-1):
        line = self.capture[num]
        return self.search(pat, line, num)

    def find(self, pat):
        num = 0
        for line in reversed(self.capture):
            num-=1
            found = self.search(pat, line, num)
            if found:
                return found

    def find_all(self, pat):
        for num, line in enumerate(self.capture):
            found = self.search(pat, line, num)
            if found:
                yield found

    def wait(self, pat, msg=None, back=1, dbg=None):
        go = True
        while go:
            sleep(1)
            out = self.capture
            if not out: continue
            for line in out[-back:]:
                if search(pat, line):
                    if dbg:
                        print(f'{dbg} : {pat} found in {line}')
                    go = False
                else:
                    if dbg:
                        print(f'{dbg} : {pat} not in {line}')
        if msg:
            print(msg)

    def run(self, cmd, exp=None, head=None, foot=None, back=1, dbg=None, raw=False):
        if head: print(head)
        self.send_keys(cmd) if raw else self.send(cmd)
        if exp: self.wait(exp, foot, back, dbg)

    def script(self, source, exp=None, head=None, foot=None, back=1, dbg=None):
        if head: print(head)

        for line in source.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                self.send(line)

        if exp:
            self.wait(exp, foot, back, dbg)
        elif foot:
            print(foot)

    def close(self):
        self.send('# Pane closing ...')
        sleep(1)
        self.send_keys('C-d')

    def __str__(self):
        return f"{self.is_active and '*' or ' '} {self.pane_title}{self.pane_id}"

