from typing import List, Callable

from .com import Com
from .consts import RetCode


class RetCom:
	def __init__(self, shell, com, args: List[str], path: str):
		self.shell = shell
		self.com: Com = com
		self.args: List[str] = args
		self.path: str = path
		self.code: RetCode = RetCode.NONE
		self.answer: str = ''

	def get_arg(self, index: int, default=None, method: Callable = str):
		# noinspection PyBroadException
		try:
			return method(self.args[index])
		except:  # NOSONAR
			return default

	def quick(self, answer='', code: RetCode = RetCode.OK) -> 'RetCom':
		self.answer = answer if isinstance(answer, str) else repr(answer)
		self.code = code
		return self

	def error(self, answer='') -> 'RetCom':
		self.answer = answer if isinstance(answer, str) else repr(answer)
		self.code = RetCode.ERROR
		return self

	def unknown(self) -> 'RetCom':
		self.answer = self.args[0] if len(self.args) else ''
		self.code = RetCode.UNKNOWN
		return self

	def empty(self):
		self.code = RetCode.EMPTY
		return self
