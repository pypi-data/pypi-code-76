from . import CheckBoxButtonGroup
from .. import Style


class Toggle(CheckBoxButtonGroup.CheckBoxButton):
	def __init__(self, master, value: bool = False, style: Style = None, text: str = '', **kw):
		super().__init__(master, style=style, text=text, **kw)
		self.set_(value)

	def get_(self):
		return self.v.get() == 1

	def set_(self, value: bool) -> None:
		self.v.set(bool(value))
