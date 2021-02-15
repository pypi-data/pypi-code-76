class Style:
	def __init__(self, /, *, bg: str = 'white', fg: str = 'black', font_family: str = None, font_size: int = 10, child: dict[str, 'Style'] = None):
		self.bg = bg if bg else None
		self.fg = fg if fg else None
		self.font_family = font_family if font_family else None
		self.font_size = font_size if font_size else None
		self.child: dict[str, Style] = {}
		if child:
			self.child = child

	def get_child(self, name, default=None) -> 'Style':
		return self.child.get(name, default)

	def alter_clone(self, bg: str = None, fg: str = None, font_family: str = None, font_size: int = 10, child: dict[str, 'Style'] = None):
		return Style(
			bg=bg if bg else self.bg,
			fg=fg if fg else self.fg,
			font_family=font_family if font_family else self.font_family,
			font_size=font_size if font_size else self.font_size,
			child=child if child else self.child
		)

	@property
	def font(self):
		return self.font_family, self.font_size

	@staticmethod
	def from_dict(in_: dict) -> 'Style':
		if 'child' in in_:
			for k, i in in_['child'].items():
				in_['child'][k] = Style.from_dict(i)
		return Style(**in_)

	def __repr__(self):
		return "<Style: " + str(self.to_dict()) + ">"

	def to_dict(self) -> dict:
		child = {}
		for k, i in self.child.items():
			child[k] = i.to_dict()
		return {
			'fg': self.fg,
			'bg': self.bg,
			'font_family': self.font_family,
			'font_size': self.font_size,
			'child': child
		}
