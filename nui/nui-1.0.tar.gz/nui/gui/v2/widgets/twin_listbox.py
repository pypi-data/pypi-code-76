from typing import List, Callable, Any

from .arch import Frame
from .basic import Listbox, Button
from .imethods import IMethods
from .. import Style


class TwinListbox(Frame, IMethods):
	def __init__(self, master, values: List = None, parse_method: Callable[[Any], str] = lambda v: repr(v), auto_width: bool = True, min_width: int = 1, height: int = 10, selectmode='single', highlightthickness: int = 0, style: Style = None, **kw):
		self.stage = master.stage
		self.style: Style = style if style else master.style
		super().__init__(master, **kw)
		self.left = Listbox(self, parse_method=parse_method, auto_width=auto_width, min_width=min_width, height=height, selectmode=selectmode, highlightthickness=highlightthickness).inline_pack(side='left', expand=True)
		self.right = Listbox(self, parse_method=parse_method, auto_width=auto_width, min_width=min_width, height=height, selectmode=selectmode, highlightthickness=highlightthickness).inline_pack(side='right', expand=True)
		self.b_to_left = Button(self, lambda: self.__switch(self.right, self.left, ), text=' < ').inline_pack(fill='both', expand=True)
		self.b_to_right = Button(self, lambda: self.__switch(self.left, self.right), text=' > ').inline_pack(fill='both', expand=True)

		if values:
			self.set_values(values)

	# noinspection PyProtectedMember
	@staticmethod
	def __switch(from_: Listbox, to_: Listbox):
		v = from_.get_()
		to_.add(v)
		for x in v:
			from_._values.remove(x)  # FIXME Too slow
		from_.set_values(from_._values)

	# noinspection PyProtectedMember
	def get_(self):
		return self.left._values

	def set_(self, value) -> None:
		self.right.set_(value)
		self.__switch(self.right, self.left)

	def set_values(self, values: List):
		self.right.set_values(values)
