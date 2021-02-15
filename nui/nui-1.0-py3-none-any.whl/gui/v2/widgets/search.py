import tkinter
from typing import Callable, Any, List

from .arch import Frame, PopUp
from .basic import Entry, Button
from .single_listbox import SingleListbox
from .. import Style


class Search(Frame):
	def __init__(self, master, values: List = None, parse_method: Callable[[Any], str] = lambda v: repr(v), auto_width: bool = True, min_width: int = 1, height: int = 10, highlightthickness: int = 0, style: Style = None, **kw):
		super().__init__(master, style, **kw)
		self.parse_method = parse_method
		self.v_search = tkinter.StringVar()
		self.v_search.trace_add("write", lambda *args: self._filter())
		self.search = Entry(self, textvariable=self.v_search).inline_pack()
		self.single_listbox = SingleListbox(self, parse_method=parse_method, auto_width=auto_width, min_width=min_width, height=height, highlightthickness=highlightthickness).inline_pack()
		self.values: List = values if values else []
		self._filter()

	def set_values(self, value: List):
		self.values = value
		self._filter()

	def set_(self, value) -> None:
		self.single_listbox.set_(value)

	def get_(self):
		self.single_listbox.get_()

	def add_items(self, value):
		self.values += value
		self._filter()

	def inline_select_bind(self, callback: Callable[[Any], None]) -> 'Search':
		self.single_listbox.inline_select_bind(callback)
		return self

	def _filter(self):  # TODO Move this to Listbox
		out = []
		for v in self.values:
			f = self.parse_method(v)
			if tkinter.re.match(r'.*{}.*'.format(tkinter.re.escape(self.search.get_())), f, tkinter.re.IGNORECASE):
				out.append(v)
		self.single_listbox.set_values(out)


class SearchPopUp(PopUp):
	def __init__(self, master, stage, close, style: Style = None, whisper=None, values=None, parse_method: Callable[[Any], str] = lambda v: repr(v), auto_width: bool = True, min_width: int = 1, height: int = 10, highlightthickness: int = 0, **kw):
		super().__init__(master, stage, close, style, whisper)
		self.search = Search(self, values, parse_method, auto_width, min_width, height, highlightthickness, style, **kw) \
			.inline_select_bind(self.selected) \
			.inline_pack()
		self.whisper = whisper

	def selected(self, value):
		self.whisper = value
		self.close()


class SearchButton(Button):
	def __init__(self, master, values: List = None, title: str = '', parse_method: Callable[[Any], str] = lambda v: repr(v), auto_width: bool = True, min_width: int = 1, height: int = 10, highlightthickness: int = 0, popup_style: Style = None, style: Style = None, **kw):
		super().__init__(master, self._pop, '', style, **kw)
		self.title = title
		self.parse_method = parse_method
		self.auto_width = auto_width
		self.min_width = min_width
		self.height = height
		self.highlightthickness = highlightthickness
		self.popup_style = popup_style

		self.__values: List = values if values else []
		self.__selected = None

	def _pop(self):
		self.stage.frame_popup(
			SearchPopUp, self.title, self.set_, self.__selected, style=self.popup_style,
			values=self.__values, parse_method=self.parse_method, auto_width=self.auto_width, min_width=self.min_width, height=self.height, highlightthickness=self.highlightthickness
		)

	def select_index(self, index: int) -> 'SearchButton':
		self.__selected = self.__values[index]
		super().set_(self.__selected)
		return self

	def get_(self):
		return self.__selected if isinstance(self.__selected, List) else [self.__selected]

	def set_(self, value) -> None:
		self.__selected = value
		super().set_('' if value is None else self.parse_method(value))

	def set_values(self, values: List):
		self.__values: List = values
