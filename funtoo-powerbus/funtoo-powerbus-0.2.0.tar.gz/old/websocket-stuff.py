#!/usr/bin/env python3

import asyncio
import logging
import os
import subprocess
from asyncio import FIRST_EXCEPTION
from datetime import datetime

from powerbus.hub import PowerBusSessionHub

hub = PowerBusSessionHub()

from powerbus.pwr_msg import PowerBusMessage
import dyne.org.funtoo.powerbus as powerbus


class FuntooIdleClient(powerbus.websocket.WebSocketClient):
	def __init__(self):
		super().__init__()
		self.ping_interval = 30 * 1000

	async def action_prepare_for_sleep(self, msg_obj):
		logging.warning("Preparing for sleep...")
		await powerbus.session.prepare_for_sleep()
		return PowerBusMessage(action=msg_obj.action, status="success")

	async def ping(self):
		out = subprocess.getoutput("/home/drobbins/development/funtoo-powerbus/xidle")
		out_msg = PowerBusMessage(
			action="ping",
			idle=int(out),
			time=datetime.utcnow(),
			USER=os.environ["USER"] if "USER" in os.environ else None,
			DISPLAY=os.environ["DISPLAY"] if "DISPLAY" in os.environ else None,
			inhibitors=await powerbus.session.get_session_inhibitors(),
		)
		print("idle =", out_msg.idle)
		await self.send(out_msg)

	async def ping_loop(self):
		while True:
			await asyncio.sleep(1)
			await self.ping()

	async def start(self):
		self.tasks.append(asyncio.create_task(self.ping_loop()))
		await super().start()


class FuntooIdleReconnectingClient:

	"""
	All this class does is create new FuntooIdleClient instances over and over again as old ones die, to re-establish
	the connection if possible. A three-second reconnection delay is used.
	"""

	def __init__(self):
		self.ws_future = None

	async def start(self):
		while True:
			self.ws_future = asyncio.create_task(FuntooIdleClient().start())
			done_list, cur_tasks = await asyncio.wait([self.ws_future], return_when=FIRST_EXCEPTION)
			self.ws_future = None
			for done_item in done_list:
				try:
					_ = done_item.result()
				except Exception as e:
					logging.warning(f"idled client exception: {e}")
			logging.warning(">> Reconnect delay...")
			await asyncio.sleep(3)
