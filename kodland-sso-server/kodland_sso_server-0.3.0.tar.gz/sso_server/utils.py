from os import urandom
from datetime import timedelta, datetime


def generate_random() -> str:
	"""
	генерация случайной строки для значения полей моделей по умолчанию
	"""
	return urandom(30).hex()


def time_slice():
	"""
	возвращает +1 день от текущего в формате даты для значения поля модели по умолчанию
	"""
	return datetime.now() + timedelta(days=1)
