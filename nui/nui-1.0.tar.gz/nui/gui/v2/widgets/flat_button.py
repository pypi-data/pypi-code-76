import tkinter
from inspect import getfullargspec
from typing import Callable

from .imethods import IMethods


class FlatButton(tkinter.Label, IMethods):
	def __init__(self, master, text: str, command: Callable, **kw):
		self.stage = master.stage
		super().__init__(master, text=text, bg=self.stage.style.bg, fg=self.stage.style.fg, **kw)
		self.bind('<Button-1>', command if getfullargspec(command).args else lambda _: command())

	def get_(self):
		return self['text']

	def set_(self, value) -> None:
		self['text'] = value
