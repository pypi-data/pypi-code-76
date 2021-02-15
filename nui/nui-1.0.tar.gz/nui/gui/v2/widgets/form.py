from typing import Type, Callable, Any, Dict, List

from .arch import Frame
from .basic import Label
from .imethods import IMethods


class Form(Frame):
	class _Field(Frame):
		def __init__(self, master, label: str, widget: Type[IMethods], b_get: Callable = lambda: '', validator: Callable[[str], bool] = None, **kw):
			super().__init__(master)
			self.label = Label(self, text=label).inline_pack(side='left')
			self.w = widget(self, **kw).inline_pack(expand=True)
			self.b_get = b_get
			self.validator = validator

		def is_valid(self) -> bool:
			return not self.validator or self.validator(self.get_())

		def get_(self) -> str:
			return self.w.get_()

		def set_(self, value) -> None:
			self.w.set_(value)

	def __init__(self, master, **kw):
		"""
		Container for Fields. Also have some tools for quick get/set for values of objects.\n
		:param master: Parent widget
		:param kw: Other tkinter options
		"""
		super().__init__(master, **kw)
		self._fields: Dict[str, Form._Field] = {}

	def add_field(self, name: Any, widget: Type[IMethods], label: str, bind_get: Callable[[], Any] = lambda: None, validator: Callable[[str], bool] = None, empty_as='', **kw) -> 'Form':
		"""
		Add field.\n
		:param name: Key used in __getitem__() (str type is recommended)
		:param widget: Class of field
		:param label: Sets the label of field
		:param bind_get: The return from this method will be used as field's value
		:param validator: Parse validator (basic function which accepts field value as str and returns if value is valid as bool)
		:param empty_as: When value is empty ('') what should form return as value (good when you need return None instead)
		:param kw: Other tkinter options (parsed to field).
		:return: self
		"""
		# noinspection PyProtectedMember
		self._fields[name] = Form._Field(self, label, widget, bind_get, validator, **kw).inline_pack(fill='x')
		return self

	def set_fields(self) -> 'Form':
		"""
		Updates all fields based on their bind_get() method.\n
		:return: self
		"""
		for f in self._fields.values():
			f.set_(f.b_get())
		return self

	def get_not_valid(self) -> List[str]:
		return [k for k, f in self._fields.items() if not f.is_valid()]

	def get_first(self, key: Any):
		value = self[key]
		if isinstance(value, List) and len(value) > 0:
			return value[0]

	def __getitem__(self, item: Any):
		"""
		Returns value of _Field by name.\n
		:param item: Name/key of the field
		:return: _Field value
		"""
		return self._fields[item].get_()
