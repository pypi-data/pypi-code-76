from typing import List, Callable, Any

from .basic import Listbox
from .. import Style


class SingleListbox(Listbox):
	def __init__(self, master, values: List = None, parse_method: Callable[[Any], str] = lambda v: repr(v), auto_width: bool = True, min_width: int = 1, height: int = 10, highlightthickness: int = 0, style: Style = None, **kw):
		super().__init__(master, values=values, parse_method=parse_method, auto_width=auto_width, min_width=min_width, height=height, selectmode=Listbox.SINGLE, highlightthickness=highlightthickness, style=style, **kw)

	def get_(self):
		if self.curselection():
			return self._values[self.curselection()[0]]
		return None

	def set_(self, value) -> None:
		if value is None:
			self.selection_clear(0, 'end')
		else:
			self.selection_set(self._values.index(value))
