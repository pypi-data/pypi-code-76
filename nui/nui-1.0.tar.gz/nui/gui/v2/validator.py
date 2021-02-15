from typing import Callable


def string(allow_chars: str = '', block_chars: str = '', allow_empty: bool = True, max_length: int = None) -> Callable[[str], bool]:
	def out(v: str) -> bool:
		if not v:
			return allow_empty
		if allow_chars or block_chars:
			for c in v:
				if (allow_chars and c not in allow_chars) or (block_chars and c in block_chars):
					return False
		if max_length is not None and len(v) > max_length:
			return False
		return True

	return out


def integer(empty: bool = True, min_value: int = None, max_value: int = None) -> Callable[[str], bool]:
	def out(v: str) -> bool:
		try:
			v = int(v)
			if min_value is not None and v < min_value:
				return False
			if max_value is not None and v > max_value:
				return False
			return True
		except Exception:
			return empty if not v else False

	return out
