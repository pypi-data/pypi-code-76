import asyncio
import logging
from datetime import datetime, timedelta
import tornado.web
import tornado.httpserver
from tornado.websocket import websocket_connect, WebSocketClosedError


class WebSocketServer(tornado.web.Application):

	http_port = 9007
	http_listen = "127.0.0.1"

	def __init__(self, handlers=None):
		super().__init__(handlers=handlers)
		self.http_server = tornado.httpserver.HTTPServer(self, xheaders=True)
		self.ws_id_map = {}

	def register_websocket(self, wshandler):
		ws_id = id(wshandler)
		logging.warning(f"*** Registering websocket: {ws_id}.")
		updated_on = datetime.utcnow()
		self.ws_id_map[ws_id] = {"handler": wshandler, "updated_on": updated_on}

	def unregister_websocket(self, wshandler):
		logging.warning(f"*** Unregistering websocket")
		ws_id = id(wshandler)
		if ws_id not in self.ws_id_map:
			return
		del self.ws_id_map[ws_id]

	def iter_sockets(self, max_age=None):
		now = datetime.utcnow()
		for ws_id, socket_data in self.ws_id_map.items():
			if max_age is None:
				yield socket_data["handler"]
			elif now - socket_data["updated_on"] <= max_age:
				yield socket_data["handler"]

	async def start(self):
		if self.http_port is not None:
			logging.info("Starting HTTP Server")
			self.http_server.bind(self.http_port, self.http_listen)
			self.http_server.start()
		while True:
			await asyncio.sleep(3)


class AppWebSocketConnection(tornado.websocket.WebSocketHandler):

	"""
	This class represents the server side of a single WebSocket connection.
	"""

	def on_close(self):
		self.application.unregister_websocket(self)

	async def on_message(self, msg_dict: str) -> None:
		msg_obj = PowerBusMessage.from_msg(msg_dict)
		self.application.register_websocket(self)
		await self.handle_message(msg_obj)

	async def send(self, msg_obj):
		await self.write_message(msg_obj.msg)

	def open(self) -> None:
		logging.warning("GOT CONNECTION")
		self.set_nodelay(True)


class WebSocketClient:

	url = "ws://127.0.0.1:9007/ws/1.0/connect"

	def __init__(self):
		self.socket = None
		self.stopped = False
		self.last_incoming_msg = datetime.utcnow()
		self.idle_timeout = timedelta(seconds=10)
		self.tasks = []

	async def start(self):
		"""
		This method will start the websocket. If any error condition is encountered (connection dropped, timeout
		waiting for response, etc.), this method will return. The idea here is that this client represents one
		specific connection, and you would have your own reconnect loop and reconnect by creating a new instance
		of this client and ``start()``ing it for a new connection.
		"""

		try:
			logging.warning(f"> Connecting to {self.url}...")
			self.socket = await websocket_connect(self.url, connect_timeout=3000)
		except ConnectionRefusedError:
			self.stopped = True

		while not self.stopped:
			if datetime.utcnow() - self.last_incoming_msg > self.idle_timeout:
				break
			try:
				msg_dict = await asyncio.wait_for(self.socket.read_message(), timeout=8)
				self.last_incoming_msg = datetime.utcnow()
			except asyncio.TimeoutError:
				continue

			if msg_dict is None:
				logging.warning("> Seems connection closed on us!")
				break

			msg_obj = PowerBusMessage.from_msg(msg_dict)
			if "action" not in msg_obj:
				logging.warning(f"Received message with no action: {msg_dict}")
				continue

			action_func = getattr(self, f"action_{msg_obj.action.replace('-', '_')}", None)
			if action_func is None:
				logging.warning(f"Received message for action {msg_obj.action}: not found.")
			else:
				resp_obj: PowerBusMessage = await action_func(msg_obj)
				if resp_obj is not None:
					await self.send(resp_obj)

		# CLEANUP ACTIONS

		for task in self.tasks:
			if not task.cancelled():
				logging.warning("CANCELLING TASK!")
				task.cancel()
		logging.warning("> WebSocketClient exiting. Socket is None.")

	async def send(self, msg_obj):
		if not self.stopped and self.socket:
			try:
				await self.socket.write_message(msg_obj.msg)
			except WebSocketClosedError:
				logging.warning("Websocket was closed so can't send message.")
				self.stopped = True
		else:
			logging.warning("Skipping message send.")
