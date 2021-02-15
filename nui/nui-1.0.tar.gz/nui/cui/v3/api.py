from .com import Com
from .consts import RetCode
from .retcom import RetCom
from .shell import Shell


# noinspection PyMethodMayBeStatic
class Api:
	def __init__(self):
		self.commands = []
		self.shell: Shell = Shell(self)
		self.rc: RetCom = RetCom(None, None, [], '')
		self.set_commands()

	def path(self):
		"""
		Overwrite me
		"""
		return ""

	def parse_args(self, arg: str) -> str:
		"""
		Overwrite me
		"""
		return arg

	def set_commands(self):
		"""
		Overwrite me
		"""
		pass

	# fun = com()(fun) NOSONAR
	def com(self, com: Com):
		"""
		Decorator around Com logic methods
		:param com: Com()
		:return: com.method if com.method else fun
		"""

		def decorator(fun):
			com.method = com.method if com.method else fun
			return fun

		self.commands.append(com)
		return decorator

	def quick_run(self, com: str):
		rc: RetCom
		for rc in self.shell.line_com_parser(com):
			if rc.code == RetCode.EXIT:
				return False
			elif rc.code == RetCode.EMPTY:
				continue
			elif rc.code == RetCode.ERROR:
				print(f"[Error] {rc.com.name}{(': ' + rc.answer) if rc.answer else ''}")
			elif rc.code == RetCode.PATH_ERROR:
				print(f"[Path Error] {rc.com.name}: {rc.answer}")
			elif rc.code == RetCode.ARGS_ERROR:
				print(f"[Args Error] {rc.com.name}{(': ' + rc.answer) if rc.answer else ''}")
			elif rc.code == RetCode.UNKNOWN:
				print(f"[Unknown command] {rc.com.name}")
			elif rc.answer:
				print(rc.answer)
		return True

	def quick_run_loop(self, add_to_path: str = '>'):
		while self.quick_run(input(f'{self.shell.path}{add_to_path}')):
			pass  # NOSONAR
