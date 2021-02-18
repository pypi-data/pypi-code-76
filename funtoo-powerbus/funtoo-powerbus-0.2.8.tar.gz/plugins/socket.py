import logging

from bson.json_util import CANONICAL_JSON_OPTIONS, dumps, loads

POWERBUS_PATH = "/run/funtoo/powerbus-socket"


class PowerBusMessage(dict):
	@property
	def msg(self):
		return dumps(self, json_options=CANONICAL_JSON_OPTIONS)

	@classmethod
	def from_msg(cls, msg):
		msgdat = loads(msg.data, json_options=CANONICAL_JSON_OPTIONS)
		return cls(**msgdat)

	async def send(self, socket):
		"""Send message to websocket"""
		msg = self.msg
		logging.debug(f"Sending message {msg}")
		await socket.send_str(msg)

	def __getattr__(self, key):
		if key not in self:
			raise AttributeError()
		return self[key]
