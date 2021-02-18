class GoogleUtilsError(Exception):
	pass

class InvalidCalculation(GoogleUtilsError):
	def __init__(self, calc: str):
		message: str = f'Invalid calculation: "{calc}"'
		super().__init__(message)

class InvalidPhrase(GoogleUtilsError):
	def __init__(self, def_: str):
		message = f'Unknown phrase: "{def_}"'
		super().__init__(message)

class InvalidLocation(GoogleUtilsError):
	def __init__(self, location: str):
		message = f'Unknown location: "{location}"'
		super().__init__(message)