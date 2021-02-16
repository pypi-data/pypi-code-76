import asyncio
import logging
import os
import random
import string
import subprocess
import sys
from collections import defaultdict
from datetime import datetime

import zmq.asyncio
from dbus_next import Message, InterfaceNotFoundError, BusType

import dyne.org.funtoo.powerbus.zmq_bus as zmq_bus
from dbus_next.aio import MessageBus

from subpop.hub import DeferredHubProperty


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


class FuntooIdleClient(object):
	def __init__(self, endpoint=zmq_bus.BUS_PATH, identity=None):
		self.endpoint = endpoint
		self.ctx = zmq.asyncio.Context()
		self.client: zmq.asyncio.Socket = self.ctx.socket(zmq.DEALER)

		# https://stackoverflow.com/questions/60324740/0mq-can-you-drop-a-message-after-a-timeout-in-a-req-rep-pattern
		# These lines, combined with a msg.send(flags=zmq.NOWAIT), will result in our client not queueing up messages
		# to the daemon if the daemon is not available. Messages will just be discarded. This prevents a flood of stale
		# messages being sent to the daemon when it starts up.

		self.client.setsockopt(zmq.LINGER, 0)
		self.client.setsockopt(zmq.IMMEDIATE, 1)
		self.client.setsockopt(zmq.CONFLATE, 1)
		self.client.setsockopt(zmq.RCVTIMEO, 1000)
		if identity is None:
			self.client.setsockopt(
				zmq.IDENTITY, ("".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16)).encode("ascii"))
			)
		else:
			self.client.setsockopt(zmq.IDENTITY, identity.encode("utf-8"))
		logging.info("Connecting to " + self.endpoint)
		self.client.connect(self.endpoint)
		self.ping_event = asyncio.Event()

	async def on_recv(self, msg):
		msg_obj = zmq_bus.PowerBusMessage.from_msg(msg)
		print("Got", msg_obj)
		action_method_name = "action_" + msg_obj.action.replace("-", "_")
		action_method = getattr(self, action_method_name, None)
		if action_method:
			resp_obj = await action_method(msg_obj)
			if resp_obj:
				# Note that this is not really a response. This is a new message "info" or "req" going out...
				await resp_obj.send(self.client)
			else:
				logging.error(f"I really did not expect this: {msg}")
		else:
			logging.error("Action method not found: %s" % action_method_name)

	async def action_prepare_for_sleep(self, msg_obj):
		logging.warning("Preparing for sleep...")
		await prepare_for_sleep()
		return zmq_bus.PowerBusMessage(action=msg_obj.action, status="success")

	async def start(self):
		await hub.add_property("SESSION_BUS", DeferredHubProperty(lambda: MessageBus(bus_type=BusType.SESSION).connect()))
		asyncio.create_task(self.ping_task())
		# await on this -- it will never end -- so this method will never end -- which is what we want:
		await self.recv_task()

	async def recv_task(self):
		while True:
			try:
				msg = await self.client.recv_multipart()
				await self.on_recv(msg)
			except zmq.ZMQError:
				# Likely no message.
				pass

	async def ping(self):
		sys.stdout.write(".")
		sys.stdout.flush()
		out = subprocess.getoutput("/usr/bin/funtoo-xidle")
		out_msg = zmq_bus.PowerBusMessage(
			action="ping",
			idle=int(out),
			time=datetime.utcnow(),
			USER=os.environ["USER"] if "USER" in os.environ else None,
			DISPLAY=os.environ["DISPLAY"] if "DISPLAY" in os.environ else None,
			inhibitors=await get_session_inhibitors(),
		)
		print("idle =", out_msg.idle)
		await out_msg.send(self.client)

	async def ping_task(self):
		while True:
			await self.ping()
			await asyncio.sleep(1)
