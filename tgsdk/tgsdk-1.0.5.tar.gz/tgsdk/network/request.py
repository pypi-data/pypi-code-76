#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2021 Evgeniy Privalov, https://linkedin.com/in/evgeniyprivalov/

try:
	import ujson as json
except ImportError:
	import json

import socket
from typing import (
	Union,
	Dict
)

import certifi
import urllib3
from urllib3.connection import HTTPConnection
from urllib3.util.timeout import Timeout

from tgsdk import (
	InputFile,
	InputMedia
)
from .errors import (
	TelegramException,
	TimeOutError,
	NetworkError,
	ChatMigrated,
	BadRequest,
	Unauthorized,
	RetryAfter,
	InvalidToken
)


class Headers:
	SERVER = "Telegram-API-SDK"
	USER_AGENT = "tgsdk (https://pypi.org/project/tgsdk/)"


class Methods:
	POST = "post"
	GET = "get"


class Request(object):
	"""

	"""
	__slots__ = ("_conn_pool_size", "_connect_timeout", "_read_timeout", "_conn_pool")

	def __init__(
		self,
		conn_pool_size: int = 10,
		connect_timeout: float = 5,
		read_timeout: float = 5
	):
		self._conn_pool_size = conn_pool_size
		self._connect_timeout = connect_timeout
		self._read_timeout = read_timeout

		socket_options = HTTPConnection.default_socket_options + [
			(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
		]
		pool_timeout = urllib3.Timeout(
			connect=self._connect_timeout,
			read=read_timeout,
			total=None
		)

		kwargs = dict(
			host="api.telegram.org",
			maxsize=self._conn_pool_size,
			cert_reqs="CERT_REQUIRED",
			ca_certs=certifi.where(),
			socket_options=socket_options,
			timeout=pool_timeout
		)

		self._conn_pool = urllib3.PoolManager(**kwargs)

	@staticmethod
	def parse(body: bytes) -> Union[Dict, bool]:
		"""
		
		:param body:
		:return: 
		"""
		try:
			data = json.loads(body.decode("utf-8", "replace"))
		except ValueError:
			raise TelegramException("Invalid response")

		if data.get("ok"):
			return data["result"]
		else:
			parameters = data.get("parameters")
			if parameters:
				migrate_to_chat_id = parameters.get("migrate_to_chat_id")
				if migrate_to_chat_id:
					raise ChatMigrated(migrate_to_chat_id)

				retry_after = parameters.get("retry_after")
				if retry_after:
					raise RetryAfter(retry_after)

			description = data.get("description")
			if description:
				return description

	def wrapper(self, *args, **kwargs):
		"""

		:param args:
		:param kwargs:
		:return:
		"""
		headers = {
			"Server": Headers.SERVER,
			"User-Agent": Headers.USER_AGENT,
			"connection": "keep-alive"
		}
		if "headers" in kwargs:
			headers.update(kwargs["headers"])

		try:
			response = self._conn_pool.request(*args, **kwargs)
		except urllib3.exceptions.TimeoutError:
			raise TimeOutError()
		except urllib3.exceptions.HTTPError as error:
			raise NetworkError("urllib3 HTTPError %s" % error)

		if 200 <= response.status <= 299:
			return response.data

		try:
			error_message = self.parse(response.data)
		except ChatMigrated:
			raise
		except RetryAfter:
			raise
		except Exception as exc:
			error_message = str(exc)

		if response.status == 400:
			raise BadRequest(error_message)
		elif response.status in (401, 403):
			raise Unauthorized(error_message)
		elif response.status == 404:
			raise InvalidToken()
		elif response.status == 413:
			# https://core.telegram.org/bots/api#senddocument

			raise NetworkError("File too large")
		elif response.status == 502:
			raise NetworkError("Bad Gateway")

		raise NetworkError("(%s) %s" % (response.status, error_message))

	def post(self, url: str, payload: Dict, timeout: float = None) -> Union[Dict, bool]:
		"""

		:param url:
		:param payload:
		:param timeout:
		:return:
		"""
		options = {}

		if timeout is not None:
			options["timeout"] = Timeout(read=timeout, connect=self._connect_timeout)

		if payload is None:
			payload = {}

		with_files = None

		for key, val in payload.items():
			if isinstance(val, InputFile):
				payload[key] = val.tuple_mapping_values

				with_files = True
			elif isinstance(val, (int, float)):
				payload[key] = str(val)
			elif key == "media":
				if isinstance(val, InputMedia):
					payload[key] = val.to_json()

					if isinstance(val.media, InputFile):
						payload[val.media.file_attach_name] = val.media.tuple_mapping_values
				else:
					media_list = []
					for media in val:
						media_dict = media.to_dict()
						media_list.append(media_dict)

						if isinstance(media.media, InputFile):
							payload[media.media.file_attach_name] = media.media.tuple_mapping_values

							if hasattr(media, "thumb"):
								payload[media.thumb.file_attach_name] = media.thumb.field_tuple

					payload[key] = json.dumps(media_list)

				with_files = True
			elif isinstance(val, list):
				payload[key] = json.dumps(val)

		if with_files:
			result = self.wrapper(
				Methods.POST,
				url,
				fields=payload,
				**options
			)
		else:
			result = self.wrapper(
				Methods.POST,
				url,
				body=json.dumps(payload).encode("utf-8"),
				headers={
					"Content-Type": "application/json"
				},
				**options,
			)

		return self.parse(result)
