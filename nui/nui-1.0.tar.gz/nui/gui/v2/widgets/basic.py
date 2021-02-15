import tkinter
from typing import Callable, List, Any, Iterable

from .imethods import IMethods
from .. import Style


class Label(tkinter.Label, IMethods):
	def __init__(self, master, text: str = '', style: Style = None, **kw):
		self.stage = master.stage
		self.style: Style = style if style else master.style
		super().__init__(master, text=text, bg=self.style.bg, fg=self.style.fg, font=self.style.font, **kw)

	def get_(self):
		return self['text']

	def set_(self, value):
		self['text'] = value


class Button(tkinter.Button, IMethods):
	def __init__(self, master, command: Callable[[], Any], text: str = '', style: Style = None, **kw):
		self.stage = master.stage
		self.style: Style = style if style else master.style
		super().__init__(master, text=text, bg=self.style.bg, fg=self.style.fg, font=self.style.font, command=command, **kw)

	def get_(self):
		return self['text']

	def set_(self, value) -> None:
		self['text'] = value


class Entry(tkinter.Entry, IMethods):
	def __init__(self, master, width: int = 1, style: Style = None, **kw):
		self.stage = master.stage
		self.style: Style = style if style else master.style
		super().__init__(master, width=width, bg=self.style.bg, fg=self.style.fg, insertbackground=self.style.fg, font=self.style.font, **kw)

	def get_(self):
		return self.get()

	def set_(self, value):
		self.delete(0, 'end')
		if value:
			self.insert('end', value)


class Text(tkinter.Text, IMethods):
	def __init__(self, master, width: int = 1, height: int = 1, style: Style = None, **kw):
		self.stage = master.stage
		self.style: Style = style if style else master.style
		super().__init__(master, width=width, height=height, bg=self.style.bg, fg=self.style.fg, insertbackground=self.style.fg, font=self.style.font, **kw)

	def get_(self):
		return self.get(1.0, 'end').strip()

	def set_(self, value):
		self.delete(1.0, 'end')
		if value:
			self.insert('end', value)


class Listbox(tkinter.Listbox, IMethods):
	SINGLE = 'single'
	MULTIPLE = 'multiple'
	BROWSE = 'browse'
	EXTENDED = 'extended'

	def __init__(self, master, values: List = None, parse_method: Callable[[Any], str] = lambda v: repr(v), auto_width: bool = True, min_width: int = 1, height: int = 10, selectmode='single', highlightthickness: int = 0, style: Style = None, **kw):
		self.stage = master.stage
		self.style: Style = style if style else master.style
		super().__init__(master, width=min_width, height=height, selectmode=selectmode, highlightthickness=highlightthickness, bg=self.style.bg, fg=self.style.fg, font=self.style.font, **kw)
		self._parse_method = parse_method
		self.min_width = min_width
		self.auto_width = auto_width
		self._values: List = values if values else []
		self.set_values(self._values)

	def get_(self):
		return [self._values[i] for i in self.curselection()]

	def set_(self, value) -> None:
		if value is None:
			self.selection_clear(0, 'end')
			return
		if isinstance(value, List):
			for v in value:
				self.selection_set(self._values.index(v))
		else:
			self.selection_set(self._values.index(value))

	def set_values(self, values: Iterable):
		self.delete(0, 'end')
		self._values = []
		self.add(values)

	def add(self, value: Iterable):
		self._values += value
		width = self.min_width
		for v in value:
			f = self._parse_method(v)
			self.insert('end', f)
			if self.auto_width and len(f) > width:
				width = len(f)
		self.min_width = int(width * 0.9)
		self.config(width=self.min_width)

	def inline_select_bind(self, callback: Callable[[Any], None]) -> 'Listbox':
		def bind_event(v):
			# 	if v: # 52 Random empty select
			callback(v)

		self.inline_bind("<Return>", lambda _: bind_event(self.__select_activated()))
		self.inline_bind("<<ListboxSelect>>", lambda _: bind_event(self.get_()))
		return self

	def __select_activated(self):  # Selected by <Return>
		if self['selectmode'] == Listbox.SINGLE:
			self.selection_clear(0, 'end')
		i = self.index('active')
		if self.selection_includes(i):
			self.selection_clear(i)
		else:
			self.selection_set(i)
		return self.get_()
