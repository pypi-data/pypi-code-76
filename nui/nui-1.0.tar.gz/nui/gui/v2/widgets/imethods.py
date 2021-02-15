import tkinter
from typing import Callable


class IMethods(tkinter.Widget):
	def is_active(self) -> bool:
		"""
		Whenever master is active.
		:return: Scene.is_active()
		"""
		return self.master.is_active()

	def inline_pack(self, /, *, fill='both', side='top', anchor='c', expand=False, **kw) -> 'super()':
		"""
		Packs it's self and returns self.\n
		:param fill: Specifies whether the widget should occupy all the space provided to it by the master. If NONE, keep the widget’s original size. If X (fill horizontally), Y (fill vertically), or BOTH (default), fill the given space along that direction. To make a widget fill the entire master widget, set fill to BOTH and expand to a non-zero value.
		:param side: Specifies which side to pack the widget against. To pack widgets vertically, use TOP (default). To pack widgets horizontally, use LEFT. You can also pack widgets along the BOTTOM and RIGHT edges.
		:param anchor: Anchor must be a valid anchor position such as n or sw; it specifies where to position each slave in its parcel. Defaults to center.
		:param expand: Specifies whether the widgets should be expanded to fill any extra space in the geometry master. If false (default), the widget is not expanded.
		:param kw: Other options (see official tkinter.Widget.pack() documentation)
		:return: self
		"""
		self.pack(fill=fill, side=side, anchor=anchor, expand=expand, **kw)
		return self

	def inline_bind(self, sequence: str = None, func: Callable[[tkinter.Widget], None] = None, add: bool = None) -> 'super()':
		"""
		Bind to this widget at event SEQUENCE a call to function FUNC.\n
		:param sequence: See official tkinter.Widget.bind() docs.
		:param func: will be called if the event sequence occurs with an instance of Event as argument. If the return value of FUNC is "break" no further bound function is invoked.
		:param add: An additional boolean parameter ADD specifies whether FUNC will be called additionally to the other bound function or whether it will replace the previous function.
		:return: self
		"""
		self.bind(sequence=sequence, func=lambda w: func(w) if self.is_active() else None, add=add)
		return self

	def get_(self):
		"""
		Returns widget value.\n
		"""
		raise Exception(f"Get method of Widget f{self.__class__}")

	def set_(self, value) -> None:
		"""
		Sets widget value.\n
		"""
		raise Exception(f"Get method of Widget f{self.__class__}")
