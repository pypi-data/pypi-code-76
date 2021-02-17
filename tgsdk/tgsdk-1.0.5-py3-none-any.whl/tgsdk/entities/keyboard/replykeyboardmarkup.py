#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2021 Evgeniy Privalov, https://linkedin.com/in/evgeniyprivalov/

from typing import (
	Dict,
	List,
	Union
)

from .keyboardbutton import KeyboardButton
from .replymarkup import ReplyMarkup


class ReplyKeyboardMarkup(ReplyMarkup):
	"""
	https://core.telegram.org/bots/api#replykeyboardmarkup

	"""
	__slots__ = ("keyboard", "resize_keyboard", "one_time_keyboard", "selective")

	def __init__(
		self,
		keyboard: List[List[Union[str, KeyboardButton]]],
		resize_keyboard: bool = False,
		one_time_keyboard: bool = False,
		selective: bool = False
	):
		self.keyboard = self.set_keyboard(keyboard)
		self.resize_keyboard = resize_keyboard
		self.one_time_keyboard = one_time_keyboard
		self.selective = selective

	@staticmethod
	def set_keyboard(keyboard: List[List[Union[str, KeyboardButton]]]) -> List[List[Union[str, KeyboardButton]]]:
		"""

		:param keyboard:
		:return:
		"""
		_keyboard = []

		for row in keyboard:
			button_row = []
			for button in row:
				if isinstance(button, KeyboardButton):
					button_row.append(button)
				else:
					button_row.append(KeyboardButton(button))

			_keyboard.append(button_row)

		return _keyboard

	def to_dict(self) -> Dict:
		"""

		:return:
		"""
		data = super().to_dict()
		data["keyboard"] = []

		for row in self.keyboard:
			row_buttons = []

			for col in row:
				if isinstance(col, KeyboardButton):
					row_buttons.append(col.to_dict())
				else:
					row_buttons.append(col)

			if row_buttons:
				data["keyboard"].append(row_buttons)

		return data
