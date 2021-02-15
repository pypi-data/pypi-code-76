from typing import List, Union, Iterable

from .consts import RetCode


class Com:
	def __init__(self, name: Union[str, List[str]], method: callable, method_args: Iterable = None, method_kwargs: dict = None, condition: callable = lambda: True, man: str = ''):
		self.name: List[str] = name if isinstance(name, List) else name.strip().split(' ')  # FIXME Spaces in list elements
		self.method: callable = method
		self.method_args: tuple = method_args if method_args else ()
		self.method_kwargs: dict = method_kwargs if method_kwargs else {}
		self.condition = condition
		self.man = man  # TODO Better help

	def run(self, api, ret_com):
		api.rc = ret_com
		if not self.condition():
			return api.rc.quick(code=RetCode.DENIED)
		elif len(api.rc.args) > 1 and api.rc.args[1] in ['help']:
			return api.rc.quick(self.man, RetCode.HELP)
		else:
			o = self.method(*self.method_args, **self.method_kwargs)
			return o if o else api.rc
