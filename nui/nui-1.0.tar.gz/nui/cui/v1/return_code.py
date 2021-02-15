import warnings

warnings.warn("ncui v1 is deprecated use newer version instead", DeprecationWarning)


# noinspection PyPep8Naming
class ReturnCode:
	EXIT = -1
	OK = 0
	UNKNOWN = 1
	ERROR = 2
	ARGS_ERROR = 3
	PATH_ERROR = 4

	def __init__(self, code: int, answer: str = None):
		self.com = None
		self.code = code
		self.answer = answer

	class ICom:
		def __init__(self, com: dict, name: str):
			self.com = com
			self.name = name
