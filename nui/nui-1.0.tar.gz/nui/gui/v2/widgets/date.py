from datetime import date

from .arch import Frame
from .basic import Entry, Label, Button
from .. import Style


class Date(Frame):
	def __init__(self, master, today_button: bool = False, style: Style = None, **kw):
		super().__init__(master, style, **kw)
		self.day = Entry(self, width=2).inline_pack(side='left')
		Label(self, '/').inline_pack(side='left')
		self.month = Entry(self, width=2).inline_pack(side='left')
		Label(self, '/').inline_pack(side='left')
		self.year = Entry(self, width=4).inline_pack(side='left')
		if today_button:
			Button(self, lambda: self.set_today(), 'Today').inline_pack(side='left')

	def set_today(self):
		self.set_(date.today())

	def get_(self):
		try:
			return date(int(self.year.get_()), int(self.month.get_()), int(self.day.get_()))
		except Exception as _:
			pass

	def set_(self, value: date) -> None:
		self.day.set_(value.day)
		self.month.set_(value.month)
		self.year.set_(value.year)
