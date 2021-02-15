import warnings
from typing import Tuple, Iterator

# noinspection PyDeprecation
from .return_code import ReturnCode  # Silence warning about deprecated code in deprecated code XD

warnings.warn("ncui v1 is deprecated use newer version instead", DeprecationWarning)


class Api:
	def started(self, sh: 'Shell') -> str:
		return ''

	def get_commands(self, force_all_commands=False) -> Tuple[list, dict]:
		return [], {'method': lambda *args: ReturnCode(ReturnCode.UNKNOWN)}

	def var_resolver(self, var: str) -> str:
		return var


class Shell:
	def __init__(self, var: Api):
		self.var = var

	def get_com(self, c: str, force_all_commands=False) -> dict:
		com, unknown = self.var.get_commands(force_all_commands)
		for n in com:
			if c in n.get('name', []):
				return n
		return unknown

	def line_com_parser(self, c: str) -> Iterator[ReturnCode]:
		for co in c.split('|'):
			co = self._com_parse(co)
			c = co[0]
			args = co[1:]

			com: dict = self.get_com(c)
			ret = com['method'](self, args)
			ret.com = ReturnCode.ICom(com, c)
			yield ret

	def _com_parse(self, c: str) -> list:
		o = []
		tmp = ''
		in_string = False
		for co in c:
			if co == ' ' and not in_string:
				if tmp:
					o.append(self.var.var_resolver(tmp))
				tmp = ''
			elif co not in ["'", '"']:
				tmp += co
			else:
				if not in_string:
					tmp = ''
				in_string = not in_string
		if tmp:
			o.append(self.var.var_resolver(tmp))
		elif not o:
			o.append('')
		return o
