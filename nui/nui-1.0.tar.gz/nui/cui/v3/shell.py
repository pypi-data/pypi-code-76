from typing import Iterator

from .com import Com
from .retcom import RetCom


class Shell:
	def __init__(self, api):
		self.api = api
		self.path: str = ''

	def _get_com(self, c: str) -> Com:  # TODO Wrapper around Commands
		for com in self.api.commands:
			if c in com.name:
				return com
		return Com('', lambda: self.api.rc.empty()) if c == '' else Com([], lambda: self.api.rc.unknown(), '')

	def line_com_parser(self, c: str) -> Iterator[RetCom]:
		for co in c.split('|'):
			co = self._com_parse(co)
			com = self._get_com(co[0])
			o: RetCom = com.run(self.api, RetCom(self, com, co, self.path))
			self.path = self.api.path()
			yield o

	def _com_parse(self, c: str) -> list:
		o = []
		tmp = ''
		in_string = False
		for co in c:
			if co == ' ' and not in_string:
				if tmp:
					o.append(self.api.parse_args(tmp))
				tmp = ''
			elif co not in ["'", '"']:
				tmp += co
			else:
				if not in_string:
					tmp = ''
				in_string = not in_string
		if tmp:
			o.append(self.api.parse_args(tmp))
		elif not o:
			o.append('')
		return o
