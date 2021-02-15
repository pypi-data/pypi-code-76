from typing import List

from .com import Com
from .consts import RetCode
from .retcom import RetCom
from .shell import Shell


# noinspection PyMethodMayBeStatic
class Api:
	def __init__(self):
		self.shell: Shell = Shell(self)
		self.rc: RetCom = RetCom(None, None, [], '')

	def get_commands(self) -> List[Com]:
		# Overwrite me
		return []

	def parse_args(self, arg: str) -> str:
		# Overwrite me
		return arg

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
