from repoly.app.client import Client
from repoly.gui.window import Window


class App:
    def __init__(self, **kwargs):
        self.window = Window(Client(), **kwargs)

    def show(self):
        self.window.show()
