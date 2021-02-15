import tkinter
from typing import Type, Dict

from .basic import IMethods
from .. import Style


class Frame(tkinter.Frame, IMethods):
	def __init__(self, master, style: Style = None, **kw):
		self.stage = master.stage
		self.style: Style = style if style else master.style
		super().__init__(master, bg=self.style.bg, **kw)

	def inline_add(self, widget: Type[tkinter.Widget], widget_kw: dict = None, pack_kw: dict = None) -> 'Frame':
		"""
		Add widget to this Frame.\n
		:param widget: widget class (not object)
		:param widget_kw: kwargs to pass to widget's __init__
		:param pack_kw: kwargs to pass to widget's pack()
		:return: self
		"""
		widget_kw = widget_kw if widget_kw else {}
		pack_kw = pack_kw if pack_kw else Frame.pack_kw_helper()
		widget(self, **widget_kw).pack(**pack_kw)
		return self

	def add(self, widget: Type[tkinter.Widget], widget_kw=None, pack_kw=None) -> tkinter.Widget:  # TODO Is tkinter.Widget correct?
		"""
		Add widget to this Frame.\n
		:param widget: widget class (not object)
		:param widget_kw: kwargs to pass to widget's __init__
		:param pack_kw: kwargs to pass to widget's pack()
		:return: widget
		"""
		widget_kw = widget_kw if widget_kw else {}
		pack_kw = pack_kw if pack_kw else {'fill': 'both'}
		o = widget(self, **widget_kw)
		o.pack(**pack_kw)  # tkinter doesn't have inline_pack()
		return o

	@staticmethod
	def pack_kw_helper(*, fill='both', side='top', anchor='c', expand=False, **kw) -> Dict:
		"""
		Little help with .pack() arguments. Mostly used in Frame.add(pack_kw=Frame.pack_kw_helper()), but can be used in normal pack methods: widget.pack(**Frame.pack_kw_helper())\n
		:param fill: Specifies whether the widget should occupy all the space provided to it by the master. If NONE, keep the widget’s original size. If X (fill horizontally), Y (fill vertically), or BOTH (default), fill the given space along that direction. To make a widget fill the entire master widget, set fill to BOTH and expand to a non-zero value.
		:param side: Specifies which side to pack the widget against. To pack widgets vertically, use TOP (default). To pack widgets horizontally, use LEFT. You can also pack widgets along the BOTTOM and RIGHT edges.
		:param anchor: Anchor must be a valid anchor position such as n or sw; it specifies where to position each slave in its parcel. Defaults to center.
		:param expand: Specifies whether the widgets should be expanded to fill any extra space in the geometry master. If false (default), the widget is not expanded.
		:param kw: Other options (see official tkinter.Widget.pack() documentation)
		:return: arguments in form of Dict
		"""
		return {'fill': fill, "side": side, "anchor": anchor, "expand": expand, **kw}


class PopUp(tkinter.Frame, IMethods):
	def __init__(self, master, stage, close, style: Style = None, whisper=None, **kw):
		self.stage = stage
		self.close = close
		self.style: Style = style if style else stage.style
		self.whisper = whisper
		super().__init__(master, bg=self.style.bg, **kw)

	def is_active(self) -> bool:
		return True
