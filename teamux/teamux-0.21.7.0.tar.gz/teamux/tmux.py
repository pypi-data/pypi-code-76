from .base import Base
from .session import Session


class Tmux(Base):
    Child = Session
    list_cmd = 'list-sessions'

    @property
    def sessions(self):
        yield from self.children

    def get(self, name):
        for s in self.sessions:
            if s.session_name==name:
                return s

    def new(self, name='xs'):
        self.tmux('new-session', '-s', name)
        return self.get(name)

    def __str__(self):
        return 'tmux'

    def tree(self):
        print('tmux')
        for s in self.sessions:
            print(' '*3, s)
            for w in s.windows:
                print(' '*6, w)
                for p in w.panes:
                    print(' '*9, p)
