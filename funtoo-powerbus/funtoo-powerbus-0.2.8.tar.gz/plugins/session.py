import asyncio
import json
import logging
import os
import pprint
import subprocess
import sys
from collections import defaultdict
from datetime import datetime

import aiohttp
import dyne.org.funtoo.powerbus as powerbus
from bson.json_util import CANONICAL_JSON_OPTIONS, loads
from dbus_next import Message, InterfaceNotFoundError, BusType
from dbus_next.aio import MessageBus


async def get_bus_names():
	"""
	This method returns a full list of bus names on the session bus. This is currently the only way to scan for
	certain buses we may be interested in.
	:return:
	:rtype:
	"""
	bus = hub.SESSION_BUS
	reply = await bus.call(
		Message(
			destination="org.freedesktop.DBus",
			path="/org/freedesktop/DBus",
			interface="org.freedesktop.DBus",
			member="ListNames",
		)
	)
	return reply.body[0]


async def pause_media_playback():
	"""
	Before going to sleep, it's a good idea to pause media playback. This will pause music playback as well as things
	like YouTube videos. Idled takes care of this directly in the user's session, by using this method.
	"""
	bus = hub.SESSION_BUS
	for bus_name in await get_bus_names():
		if bus_name.startswith("org.mpris.MediaPlayer2."):
			introspection = await bus.introspect(bus_name, "/org/mpris/MediaPlayer2")
			obj = bus.get_proxy_object(bus_name, "/org/mpris/MediaPlayer2", introspection)
			try:
				iface = obj.get_interface("org.mpris.MediaPlayer2.Player")
				await iface.call_pause()
			except InterfaceNotFoundError:
				pass


async def get_session_inhibitor(inhibitor_obj_path):
	"""
	This method extracts detailed data from a specific GNOME inhibitor -- specifically, it looks at bit flags to
	determine if the inhibitors block 'sleep' or 'idle'.
	:param inhibitor_obj_path:
	:type inhibitor_obj_path:
	:return: a tuple consisting of the app name, and then the kind of inhibitors. We only return something if we
	         find an idle or sleep inhibitor. We will return None, None if nothing we are interested in is found.
	:rtype: tuple
	"""
	bus = hub.SESSION_BUS
	bus_name = "org.gnome.SessionManager"
	introspection = await bus.introspect(bus_name, inhibitor_obj_path)
	obj = bus.get_proxy_object(bus_name, inhibitor_obj_path, introspection)
	iface = obj.get_interface("org.gnome.SessionManager.Inhibitor")
	bitwise_flags = await iface.call_get_flags()
	kinds = set()
	if bitwise_flags & 4 != 0:
		kinds.add("sleep")
	if bitwise_flags & 8 != 0:
		kinds.add("idle")
	if not len(kinds):
		return None, None
	return str(await iface.call_get_app_id()), ",".join(sorted(list(kinds))) + ": " + str(await iface.call_get_reason())


async def get_session_inhibitors():
	"""
	This method returns any inhibitors that are active in GNOME. These can block sleep.

	There are also lower-level logind inhibitors, which are handled by powerbus, not idled.
	"""
	bus = hub.SESSION_BUS
	bus_name = "org.gnome.SessionManager"
	path = "/" + bus_name.replace(".", "/")
	introspection = await bus.introspect(bus_name, path)
	obj = bus.get_proxy_object(bus_name, path, introspection)
	iface = obj.get_interface(bus_name)
	try:
		inhibitor_objs = await iface.call_get_inhibitors()
	except AttributeError:
		return {}
	inhibitor_info = defaultdict(list)
	for inhibitor_obj_path in inhibitor_objs:
		app, reason = await get_session_inhibitor(inhibitor_obj_path)
		if app is None:
			continue
		inhibitor_info[app].append(reason)
	return dict(inhibitor_info)


async def lock_screensaver():
	"""
	This method is used by idled to find a screensaver and activate its screen lock.
	"""
	bus = hub.SESSION_BUS
	screensaver_list = [
		"org.gnome.ScreenSaver",
		"org.cinnamon.ScreenSaver",
		"org.kde.screensaver",
		"org.xfce.ScreenSaver",
	]
	dbus_names = await get_bus_names()
	found_names = []
	for ss in screensaver_list:
		if ss in dbus_names:
			found_names.append(ss)
	if not len(found_names):
		logging.warning("Unable to find any active screensaver to lock.")
		return
	elif len(found_names) > 1:
		logging.warning(f"Found multiple active screensavers! {found_names}. Activating first.")
	ss_name = found_names[0]

	path = "/" + ss_name.replace(".", "/")
	introspection = await bus.introspect(ss_name, path)
	obj = bus.get_proxy_object(ss_name, path, introspection)
	iface = obj.get_interface(ss_name)
	if ss_name == "org.cinnamon.ScreenSaver":
		await iface.call_lock("funtoo")
	else:
		await iface.call_lock()


async def prepare_for_sleep():
	"""
	This is the main method that idled calls to prepare for sleep, which will currently pause media playback
	and also lock the screen.
	"""
	await pause_media_playback()
	await lock_screensaver()


class FuntooStatusClient(object):
	def __init__(self):
		self.ws = None

	async def connect(self):
		try:
			conn = aiohttp.UnixConnector(path=powerbus.socket.POWERBUS_PATH)
			async with aiohttp.ClientSession(connector=conn) as session:
				async with session.get("http://socket/status") as resp:
					json_dict = json.loads(await resp.text())
					print(json.dumps(json_dict, indent=4))
		except (aiohttp.ClientConnectionError, ConnectionResetError) as e:
			logging.error("Connection error.")


class FuntooIdleClient(object):
	def __init__(self):
		self.last_msg = datetime.utcnow()
		self.ws = None
		self.running = True

	async def connect(self):
		while True:
			try:
				logging.warning("Connecting to remote.")
				conn = aiohttp.UnixConnector(path=powerbus.socket.POWERBUS_PATH)
				async with aiohttp.ClientSession(connector=conn) as session:
					async with session.ws_connect("http://sock/ws") as self.ws:

						logging.warning("Got websocket.")
						while True:
							await self.sendinfo()
							try:
								msg = await asyncio.wait_for(self.ws.receive(), timeout=2)
							except asyncio.futures.TimeoutError:
								logging.warning("Receive timeout.")
								continue
							self.last_msg = datetime.utcnow()
							if msg.type == aiohttp.WSMsgType.TEXT:
								msg_obj = await self.on_recv(msg)
								if msg_obj is not None:
									await msg_obj.send(self.ws)
							elif msg.type == aiohttp.WSMsgType.ERROR:
								raise ConnectionResetError()
							elif msg.type == aiohttp.WSMsgType.PING:
								sys.stdout.write(".")
								sys.stdout.flush()
			except (aiohttp.ClientConnectionError, ConnectionResetError) as e:
				logging.warning(e)
				logging.warning("reconnecting in 2 seconds...")
				await asyncio.sleep(2)

	async def on_recv(self, msg) -> powerbus.socket.PowerBusMessage:
		msg_obj = powerbus.socket.PowerBusMessage.from_msg(msg)
		self.last_msg = datetime.utcnow()
		action_method_name = "action_" + msg_obj.action.replace("-", "_")
		action_method = getattr(self, action_method_name, None)
		if action_method:
			resp_obj = await action_method(msg_obj)
			if resp_obj:
				# Note that this is not really a response. This is a new message "info" or "req" going out...
				await resp_obj.send(self.ws)
			else:
				logging.error(f"I really did not expect this: {msg}")
		else:
			logging.error("Action method not found: %s" % action_method_name)

	async def action_prepare_for_sleep(self, msg_obj):
		logging.warning("Preparing for sleep...")
		await prepare_for_sleep()
		self.running = False
		return powerbus.socket.PowerBusMessage(action=msg_obj.action, status="success")

	async def start(self):
		hub.SESSION_BUS = await MessageBus(bus_type=BusType.SESSION).connect()
		await self.connect()

	async def sendinfo(self):
		out = subprocess.getoutput("/usr/bin/funtoo-xidle")
		out_msg = powerbus.socket.PowerBusMessage(
			action="ping",
			idle=int(out),
			time=datetime.utcnow(),
			USER=os.environ["USER"] if "USER" in os.environ else None,
			DISPLAY=os.environ["DISPLAY"] if "DISPLAY" in os.environ else None,
			inhibitors=await get_session_inhibitors(),
		)
		logging.warning(f"idle = {out_msg.idle}")
		await out_msg.send(self.ws)
