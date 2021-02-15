from enum import Enum, auto


class RetCode(Enum):
	NONE = auto()
	EMPTY = auto()
	EXIT = auto()
	OK = auto()
	HELP = auto()
	UNKNOWN = auto()
	ERROR = auto()
	ARGS_ERROR = auto()
	PATH_ERROR = auto()
	DENIED = auto()
