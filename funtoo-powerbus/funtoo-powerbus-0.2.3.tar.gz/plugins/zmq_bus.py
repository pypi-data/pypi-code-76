#!/usr/bin/python3

import zmq.asyncio
from bson.json_util import loads, CANONICAL_JSON_OPTIONS, dumps


BUS_PATH = "ipc:///run/funtoo/powerbus-socket"


class PowerBusMessage(dict):
	@property
	def msg(self):
		return dumps(self, json_options=CANONICAL_JSON_OPTIONS).encode("utf-8")

	@classmethod
	def from_msg(cls, msg):
		if isinstance(msg, list):
			msg = msg[0]
		print("msg is", msg)
		msgdat = loads(msg, json_options=CANONICAL_JSON_OPTIONS)
		return cls(**msgdat)

	async def send(self, socket, identity=None):
		"""Send message to socket"""
		msg = [self.msg]
		if identity:
			msg = [identity] + msg
		try:
			await socket.send_multipart(msg, flags=zmq.NOBLOCK)
		except zmq.ZMQError:
			print("Destination not there... dropping message....")

	def __getattr__(self, key):
		if key not in self:
			raise AttributeError()
		return self[key]
