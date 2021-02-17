from .base import Base
from .window import Window


class Session(Base):
    keys = '''
        session_id
        session_name
        session_attached
    '''
    Child = Window
    list_cmd ='list-windows'

    def __init__(self, tmux, fields):
        self.Tmux = tmux
        self.fields = fields

    @property
    def windows(self):
        yield from self.children

    def get(self, name):
        for w in self.windows:
            if w.window_name==name:
                return w

    def new(self, name='xw'):
        self.tmux(f'new-window', '-n', name)
        return self.get(name)

    @property
    def is_active(self):
        return getattr(self, 'session_attached')=='1'

    def __str__(self):
        f = self.fields
        return f"{self.is_active and '*' or ' '} {f.session_name}"

