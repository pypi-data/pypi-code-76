#!/usr/bin/env python3

import asyncio
import logging
import os
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from enum import Enum

import aiohttp
import colorama
from aiohttp import web
from bson.json_util import CANONICAL_JSON_OPTIONS, dumps
from dbus_next import Message, BusType
from dbus_next.aio import MessageBus

LID_CLOSED_EVENT = asyncio.Event()
LID_LAST_CLOSED = None
LID_LAST_OPENED = None

import dyne.org.funtoo.powerbus as powerbus


# TODO: handle scenario where lid is already closed, and AC adapter unplugged. Grab AC event and then
#       do an accelerated sleep?


def get_file(fn):
	"""
	A simple method to retrieve the contents of a file, or return None if the file does not exist.
	"""
	if not os.path.exists(fn):
		return None
	with open(fn, "r") as foo:
		return foo.read().strip()


def put_file(fn, content):
	with open(fn, "w") as foo:
		foo.write(content)


def on_ac_power():
	"""
	Will return True if on AC mains power, and False if not on AC mains power.

	Will return None if this cannot be determined (on desktop systems that do not report AC mains power.)
	:return: True, False or None.
	"""
	dn = "/sys/class/power_supply"
	if not os.path.isdir(dn):
		return None
	ac_mains_path = None
	with os.scandir(dn) as scan:
		for ent in scan:
			if not ent.is_dir():
				continue
			tpath = os.path.join(ent.path, "type")
			pow_type = get_file(tpath)
			if pow_type != "Mains":
				continue
			ac_mains_path = ent.path
			break
	if ac_mains_path is None:
		return None
	return int(get_file(os.path.join(ac_mains_path, "online"))) == 1


async def get_upower_property(prop):
	"""
	This method retrieves a property from upower on the system bus.
	"""
	bus = hub.SYSTEM_BUS
	bus_name = "org.freedesktop.UPower"
	path = "/" + bus_name.replace(".", "/")
	introspection = await bus.introspect(bus_name, path)
	obj = bus.get_proxy_object(bus_name, path, introspection)
	iface = obj.get_interface("org.freedesktop.UPower")
	return await getattr(iface, f"get_{prop}")()


async def get_logind_property(prop):
	"""
	This method retrieves a property from logind on the system bus.
	"""
	bus = hub.SYSTEM_BUS
	bus_name = "org.freedesktop.login1"
	path = "/" + bus_name.replace(".", "/")
	introspection = await bus.introspect(bus_name, path)
	obj = bus.get_proxy_object(bus_name, path, introspection)
	iface = obj.get_interface("org.freedesktop.login1.Manager")
	return await getattr(iface, f"get_{prop}")()


async def lid_is_closed():
	"""
	This will report, as of right this moment -- is the system's lid closed? A boolean is returned. Note that
	we don't use this for handling the event of the lid being closed -- see ``setup_lid_callback()`` for
	that -- because the callback gives us a real-time *event* for when the lid is closed. But this method
	can be used after to confirm -- right before sleep -- that indeed the lid is still closed.
	:return: A boolean indicating if the lid is closed (True) or open (False)
	:rtype: bool
	"""
	return await get_logind_property("lid_closed")


async def sleep_inhibited_simple():
	"""
	A simpler implementation of ``sleep_inhibited()`` for when we don't have to ignore any inhibitors.
	See below for more info.
	"""
	blocked = (await get_logind_property("block_inhibited")).split(":")
	return "sleep" in blocked


async def sleep_inhibited():
	"""
	This method looks at lower-level logind inhibitors to see if anyone is inhibiting us from going to sleep.

	We have the option to ignore some of these inhibitors. If we aren't ignoring anyone, we just use
	``sleep_inhibited_simple()`` as it is faster and simpler. We may want to ignore gnome sleep inhibition
	in some cases.

	Also note that in addition to logind inhibitors which exist on the *system* bus, there are also higher-level,
	GNOME inhibitors which are per-session and handled on the *session* bus. The latter are reported back by idled,
	and not read directly by powerbus.
	"""
	bus = hub.SYSTEM_BUS
	if powerbus.model.ignore_inhibit is None:
		return await sleep_inhibited_simple()
	bus_name = "org.freedesktop.login1"
	path = "/" + bus_name.replace(".", "/")
	reply = await bus.call(
		Message(destination=bus_name, path=path, interface="org.freedesktop.login1.Manager", member="ListInhibitors")
	)
	for thing in reply.body[0]:
		# Allow skipping of certain inhibitors
		daemon_pid = thing[5]
		try:
			daemon = os.readlink(f"/proc/{daemon_pid}/exe")
			if os.path.basename(daemon) in powerbus.model.ignore_inhibit:
				continue
		except (IOError, FileNotFoundError):
			continue
		what = thing[0]
		mode = thing[3]
		if "sleep" in what.split(":") and mode == "block":
			return True
	return False


class SleepState(Enum):
	ACTIVE = 1
	SLEEPING = 2
	ACCEL_SLEEP = 3


async def setup_lid_callback():
	"""
	This method will set up a realtime callback that gets called when the system's 'lid' is opened or closed, so
	we get real-time updates. When an open or close occurs, ``LID_LAST_CLOSED`` or ``LID_LAST_OPENED`` is updated
	with the current timestamp, and for a lid closed event, the ``LID_CLOSED_EVENT`` is triggered. This is the only
	event that powerbus really cares about -- as when a lid is closed, then we are potentially going to sleep very
	soon (we wake from sleep automatically when lid is opened, so powerbus doesn't need to handle that event.)

	This method returns right away but does ensure the callback is active and running as an async task.
	"""
	bus = hub.SYSTEM_BUS

	def upower_callback(obj_name, my_dict, *args):
		global LID_LAST_OPENED
		global LID_LAST_CLOSED
		global LID_CLOSED_EVENT
		my_dict = dict(my_dict)
		if "LidIsClosed" in my_dict:
			if my_dict["LidIsClosed"].value:
				logging.warning("Lid is closed!")
				LID_LAST_CLOSED = get_utc_time()
				LID_CLOSED_EVENT.set()
				LID_CLOSED_EVENT.clear()
			else:
				LID_LAST_OPENED = get_utc_time()

	bus_name = "org.freedesktop.UPower"
	path = "/" + bus_name.replace(".", "/")
	introspection = await bus.introspect(bus_name, path)
	obj = bus.get_proxy_object(bus_name, path, introspection)
	props = obj.get_interface("org.freedesktop.DBus.Properties")
	props.on_properties_changed(upower_callback)


class PowerBusDaemon(object):
	def __init__(self):

		# PowerBus Internals Setup:
		self.suspend_index = 0
		self.idle_delay_sec = 90
		self.last_maybe_accelerated_sleep = None
		self.last_accelerated_sleep = None
		self.has_lid = None
		self.lid_closed_accelerated_sleep = False
		self.lid_closed_idle_delay_ms = 500
		self.client_stale_timeout = timedelta(seconds=10)
		self.daemon_start = self.last_sleep_attempt = get_utc_time()
		self.next_sleep_attempt = self.last_sleep_attempt + timedelta(self.idle_delay_sec)
		self.clients = {}
		self.epoch = datetime.utcfromtimestamp(0)
		self.stale_msg_interval = timedelta(milliseconds=500)
		self.last_zero = get_utc_time()
		self.state = SleepState.ACTIVE
		self.app = None
		self.server = None
		self.runner = None
		if not self.is_root:
			raise PermissionError()

	async def stop_server(self):
		await self.runner.cleanup()

	async def start_server(self):
		"""
		This method starts the server as a background Task, and returns.
		"""

		async def status_handler(request):
			return web.Response(text=dumps(await self.status_json(), json_options=CANONICAL_JSON_OPTIONS))

		async def websocket_handler(request):
			logging.warning("Got connection!")
			ws = web.WebSocketResponse()
			await ws.prepare(request)

			async for msg in ws:
				logging.warning(f"Got message! {msg.data}")
				if msg.type == aiohttp.WSMsgType.TEXT:
					msg_obj = await self.on_recv(ws, msg)
					if msg_obj is not None:
						await msg_obj.send(ws)
				elif msg.type == aiohttp.WSMsgType.ERROR:
					logging.warning(f"ws connection closed with exception {ws.exception()}")
					self.remove_client(ws)
					break

			self.remove_client(ws)
			# connection closed
			return ws

		if not self.is_root:
			raise PermissionError()

		if not os.path.isdir("/run"):
			raise FileNotFoundError("/run not found and required by funtoo-powerbus.")
		os.umask(0o022)
		if not os.path.exists("/run/funtoo"):
			os.mkdir("/run/funtoo", 0o755)
		os.chmod("/run/funtoo", 0o755)
		os.chown("/run/funtoo", 0, 0)
		try:
			put_file("/run/funtoo/powerbus.pid", str(os.getpid()))
		except PermissionError:
			raise PermissionError("Unable to write PID file at /run/funtoo/powerbus.pid.")

		self.app = web.Application()
		self.app.add_routes([web.get("/ws", websocket_handler), web.get("/status", status_handler)])
		self.runner = web.AppRunner(self.app)
		await self.runner.setup()
		os.umask(0o000)
		site = web.UnixSite(self.runner, path=powerbus.socket.POWERBUS_PATH)
		await site.start()
		os.umask(0o022)
		logging.debug(f"Listening for new client connections at {powerbus.socket.POWERBUS_PATH}")

	@property
	def is_root(self):
		return os.geteuid() == 0

	def go_to_sleep(self):
		self.last_zero = None
		self.state = SleepState.SLEEPING
		subprocess.getoutput("echo -n mem > /sys/power/state")

	async def send_ping_to_all_active_clients(self):
		cur_time = get_utc_time()
		for client_key, datums in self.clients.items():
			ws, orig_msg_obj = datums
			if cur_time - orig_msg_obj.time <= self.client_stale_timeout:
				await ws.ping()

	async def send_message_to_all_active_clients(self, msg_obj: powerbus.socket.PowerBusMessage):
		cur_time = get_utc_time()
		for client_key, datums in self.clients.items():
			ws, orig_msg_obj = datums
			if cur_time - orig_msg_obj.time <= self.client_stale_timeout:
				logging.warning("Sending message", msg_obj)
				await msg_obj.send(ws)

	async def tell_clients_to_prepare_for_sleep(self):
		msg_obj = powerbus.socket.PowerBusMessage(action="prepare-for-sleep")
		await self.send_message_to_all_active_clients(msg_obj)

	@property
	def num_clients(self):
		num_fresh_clients = 0
		cur_time = get_utc_time()
		for client_key, datums in self.clients.items():
			ws, msg_obj = datums
			if cur_time - msg_obj.time <= self.client_stale_timeout:
				num_fresh_clients += 1
		return num_fresh_clients

	def sufficiently_idle(self, timeout_ms):

		"""
		This method will look at all non-stale clients connected, and look at their idle times. If there is at least
		one actively communicating client, and all clients' idle times are sufficient, then we will return True.
		Otherwise False.

		This doesn't mean we will definitely go to sleep, because sleep could be inhibited via logind. But we can now
		proceed to see if it's bed time.

		:return: Whether or not the system is sufficiently idle to go to sleep.
		:rtype: bool
		"""

		# This means we are recovering from sleep:

		if self.last_zero is None or self.state == SleepState.SLEEPING:
			return False

		num_fresh_clients = 0
		num_idle_clients = 0
		cur_time = get_utc_time()

		timeout_delta = timedelta(milliseconds=timeout_ms)

		# Our first test -- we must be at least timeout_ms away from our self.last_zero point. This timer gets reset
		# when certain special events happen (daemon start, resume from sleep...)

		if cur_time - self.last_zero < timeout_delta:
			# Not enough time has passed.
			return False

		# Now let's look at each client reporting idle data back to us.

		for client_key, datums in self.clients.items():
			ws, msg_obj = datums
			# We expect the client's last idle message to be at least somewhat fresh. Otherwise we'll skip it.

			time_offset = cur_time - msg_obj.time

			if time_offset > self.client_stale_timeout:
				continue

			num_fresh_clients += 1

			# Now, let's see if this client is sufficiently idle, according to our standards. msg_obj.idle stores the idle time
			# of the user, in milliseconds.

			idle = timedelta(milliseconds=msg_obj.idle)

			# Correct for the time passed since we received this message:

			idle += time_offset

			if idle > timeout_delta:
				num_idle_clients += 1

		if 0 < num_fresh_clients == num_idle_clients:
			return True
		else:
			return False

	def session_sleep_inhibited(self):
		user_inhibited = {}
		for client_key, datums in self.clients.items():
			ws, msg_obj = datums
			if len(msg_obj.inhibitors):
				user_inhibited[client_key] = msg_obj.inhibitors
		return len(user_inhibited) > 0, user_inhibited

	async def start(self):
		hub.SYSTEM_BUS = await MessageBus(bus_type=BusType.SYSTEM).connect()
		self.has_lid = await get_upower_property("lid_is_present")
		if self.has_lid:
			await setup_lid_callback()
		asyncio.create_task(self.state_manager())
		asyncio.create_task(self.sleep_handler())
		asyncio.create_task(self.lid_event_monitor_task())
		asyncio.create_task(self.status_display())
		asyncio.create_task(self.stale_cleanup_task())
		await self.start_server()
		while True:
			# ASCII heartbeat
			sys.stdout.write(".")
			sys.stdout.flush()
			await asyncio.sleep(1)

	def get_epoch_seconds(self, dt):
		return (dt - self.epoch).total_seconds()

	def utc_to_local(self, utc_dt):
		if utc_dt is None:
			return "None"
		return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

	async def will_consider_natural_sleep(self, ignore_system_inhibit=True):
		"""
		This method will tell us whether we will consider taking a nap. This is called "natural sleep", which
		means just falling asleep due to regular circumstances -- i.e. not a lid close event -- just something
		like being idle for too long and being on battery.

		This method looks at how many clients are connected (we require at least one idled connection to even
		consider natural sleep), as well as whether we are sleep inhibited through logind, or sleep inhibited
		through a GNOME session. We will also see if we are on battery power or not.

		This method doesn't actually let us know if we *will* go to sleep -- it just lets us know if we
		would *consider* going to sleep. This is useful to know -- if the system is avoiding going to sleep,
		it is good to know why.

		:return: tuple: a boolean indicating whether we will consider natural sleep, and a "reason" (string)
		  if we are not considering sleep to understand why (or None if the boolean is True)
		:rtype:
		"""
		ac = on_ac_power()
		if ac is None:
			return False, "No battery"
		if self.num_clients == 0:
			return False, "zero clients -- at least one idled client must be connected"
		if not ignore_system_inhibit and await sleep_inhibited():
			return False, "system inhibited from sleep"
		session_inhibited, _ = self.session_sleep_inhibited()
		if session_inhibited:
			return False, "user session(s) inhibiting sleep"
		if ac is False:
			return True, None
		elif ac is True:
			return False, "on AC power"
		else:
			return False, "desktop"

	def color(self, out_bool, txt=None):
		if txt is None:
			txt = out_bool
		if out_bool is True:
			out_bool = f"{colorama.Fore.GREEN}{txt}"
		elif out_bool is False:
			out_bool = f"{colorama.Fore.RED}{txt}"
		else:
			out_bool = f"{colorama.Fore.YELLOW}{txt}"
		return out_bool + colorama.Style.RESET_ALL

	async def stale_cleanup_task(self):
		while True:
			await asyncio.sleep(5)
			cur_time = get_utc_time()
			new_clients = {}
			for client_key, datums in self.clients.items():
				ws, msg_obj = datums
				if cur_time - msg_obj.time > self.client_stale_timeout:
					continue
				new_clients[client_key] = datums
			self.clients = new_clients

	async def lid_event_monitor_task(self):

		# TODO: right now, we just ignore handling the lid close event if we are on AC power. But an advanced
		#       feature we might want is the option to go to sleep if lid is closed with NO EXTERNAL DISPLAYS
		#       and we are on AC power. But I don't think that's needed for 1.0.

		while True:
			await LID_CLOSED_EVENT.wait()
			if not on_ac_power():
				self.last_maybe_accelerated_sleep = get_utc_time()
				self.lid_closed_accelerated_sleep = True
				logging.warning("We might go to sleep due to lid closed!")

	async def state_manager(self):
		"""
		This state manager is designed to pull the system out of a SLEEPING state on resume.

		When the system goes to sleep, self.state == SleepState.SLEEPING and self.last_zero is None.
		After one second, in this state, we will set self.state to SleepState.ACTIVE. Then after another
		second, self.last_zero will be set to the current time.

		Since we set the SLEEPING state and the last zero of None right before sleep, and the system
		will sleep after milliseconds, and this will take 2 seconds to go back to fully active mode,
		we will become fully active only AFTER we have resumed. And if for some reason going to sleep
		fails, this pulls us back into an active state in 2 seconds.
		"""
		while True:
			await asyncio.sleep(1)
			if self.state == SleepState.SLEEPING:
				self.state = SleepState.ACTIVE
			elif self.state == SleepState.ACTIVE:
				if self.last_zero is None:
					self.last_zero = get_utc_time()

	async def sleep_handler(self):
		"""
		This method actually sees if we should go to sleep -- now -- and if so, will put the system to sleep.
		It contains the important logic for determining this, all in one central place. This is one of the
		important goals of powerbus -- to have all this logic in one place where it can be easily understood,
		and modified or enhanced if desired.
		"""
		while True:
			# We are not fully awake yet -- so don't consider sleeping.
			if self.state == SleepState.SLEEPING or self.last_zero is None:
				await asyncio.sleep(2)
				continue

			await self.send_ping_to_all_active_clients()
			await asyncio.sleep(2)

			# We use timeout_ms set to a value to indicate that we have determined that we should consider sleep
			# as long as all our clients are sufficiently idle according to this timeout.

			timeout_ms = None

			# We consider a lid-closed accelerated sleep simply if the flag is set -- if we have received a lid-
			# close event. We will not look at any sleep inhibitors in this case. This may be different from how
			# other power management behaves, but is what we want to do for powerbus.

			# TODO: if we come back from the lid being opened, we may get some clients reporting back a significant
			#       idle time. We want to make sure we still will only consider going back to sleep after
			#       TIME_OF_RESUME + self.idle_delay_sec -- in other words, we can't look at the minimum raw
			#       idle time we get back from our idled clients -- we have to *adjust* this time based on the
			#       time of resume. This will prevent a lid-open-but-system-goes-right-back-to-sleep condition.

			if self.has_lid and self.lid_closed_accelerated_sleep:
				logging.debug("Considering accelerated sleep")
				# let's really make sure the lid is still closed, and if it's not, let's not try to sleep very soon!
				if await lid_is_closed():
					logging.debug("Lid is still closed")
					# OK, lid is really closed -- so we will try to go to sleep very soon.
					timeout_ms = self.lid_closed_idle_delay_ms
				else:
					logging.debug("Lid closed false alarm!")
					# False alarm!
					self.lid_closed_accelerated_sleep = False

			if not timeout_ms:

				# If we've gotten here, we're not doing an accelerated lid-close sleep. So we need to see if we
				# should do a natural sleep. First, let's see if we should even consider a natural sleep. This will
				# consider number of clients connected, whether we are on AC power or not, and any sleep inhibitors
				# (logind or GNOME.)

				sleep, reason = await self.will_consider_natural_sleep()
				if not sleep:
					continue

				timeout_ms = self.idle_delay_sec * 1000

			# OK, at this point, timeout_ms is set to a value. If all clients are sufficiently idle.

			sufficient_idle = self.sufficiently_idle(timeout_ms)

			if not sufficient_idle:
				continue

			if self.has_lid and self.lid_closed_accelerated_sleep:
				logging.debug("Prepping for accelerated sleep")
				# We are about to sleep, and this is an "accelerated" sleep due to the lid being closed.
				# Therefore, update the timestamp for the last accelerated sleep, and also turn off accel.
				# sleep mode -- it can only be active for one shot, then it gets disabled until the lid is
				# closed again.
				self.last_accelerated_sleep = get_utc_time()
				self.lid_closed_accelerated_sleep = False
			else:
				self.last_sleep_attempt = get_utc_time()
			logging.debug("Starting sleep!")
			await self.tell_clients_to_prepare_for_sleep()
			await asyncio.sleep(0.25)
			self.go_to_sleep()

	async def status_json(self):
		out_json = {}
		sleep, reason = await self.will_consider_natural_sleep()
		out_json["natural_sleep"] = sleep
		out_json["natural_sleep_reason"] = reason
		out_json["has_lid"] = self.has_lid
		out_json["times"] = {
			"daemon_start": self.daemon_start,
			"last_zero": self.last_zero,
			"lid_last_closed": LID_LAST_CLOSED,
			"lid_last_opened": LID_LAST_OPENED,
			"last_maybe_accel": self.last_maybe_accelerated_sleep,
			"last_accel_sleep": self.last_accelerated_sleep,
			"last_sleep": None if self.last_sleep_attempt == self.daemon_start else self.last_sleep_attempt,
		}
		for key, val in out_json["times"].items():
			if val is not None:
				out_json["times"][key] = str(val)
		out_json["state"] = str(self.state)
		out_json["clients"] = self.clients
		out_json["on_ac"] = on_ac_power()
		out_json["ignore_inhibit"] = powerbus.model.ignore_inhibit
		out_json["sleep_inhibit"] = await sleep_inhibited()
		session_inhibit, inhibitors = self.session_sleep_inhibited()
		out_json["session_inhibit"] = session_inhibit
		out_json["session_inhibitors"] = inhibitors
		return out_json

	async def status_display(self):
		while True:
			print(colorama.ansi.clear_screen())
			print(colorama.Cursor.POS())
			print(f"{colorama.Fore.CYAN}=========================={colorama.Style.RESET_ALL}")
			print(f"{colorama.Fore.CYAN}Funtoo PowerBus Statistics{colorama.Style.RESET_ALL}")
			print(f"{colorama.Fore.CYAN}=========================={colorama.Style.RESET_ALL}")
			print()
			sleep, reason = await self.will_consider_natural_sleep()
			if sleep is True:
				print(
					f" * {colorama.Fore.CYAN}Status:{colorama.Style.RESET_ALL} Will naturally sleep after {self.color(self.idle_delay_sec)} seconds of idle"
				)
			else:
				print(
					f" * {colorama.Fore.CYAN}Status:{colorama.Style.RESET_ALL} Will not naturally sleep. Reason: {self.color(reason)}"
				)
			print(f" * Daemon start time:  {self.color(self.utc_to_local(self.daemon_start))}")
			print(f" * Last zero:          {self.color(self.utc_to_local(self.last_zero))}")
			print(f" * State:              {self.color(self.state)}")
			if self.has_lid:
				print(f" * Lid Last Closed:    {self.color(self.utc_to_local(LID_LAST_CLOSED))}")
				print(f" * Lid Last Opened:    {self.color(self.utc_to_local(LID_LAST_OPENED))}")
				print(f" * Last Maybe Accel:   {self.color(self.utc_to_local(self.last_maybe_accelerated_sleep))}")
				print(f" * Last Accel Sleep:   {self.color(self.utc_to_local(self.last_accelerated_sleep))}")
				print(f" * Lid is Closed?:     {self.color(await lid_is_closed())}")
			else:
				print(f" * {self.color('No lid detected.')} Accelerated sleep via lid close disabled.")
			if self.last_sleep_attempt == self.daemon_start:
				last_sleep = None
			else:
				last_sleep = self.utc_to_local(self.last_sleep_attempt)
			print(f" * Last sleep attempt: {self.color(last_sleep)}")
			print(
				f" * There are currently {self.color(len(self.clients))} connected (cleanup interval: {self.client_stale_timeout.seconds} secs)"
			)
			on_ac = on_ac_power()
			if on_ac is None:
				out = "No battery"
			elif on_ac is True:
				out = "Laptop (on AC power)"
			else:
				out = "Laptop (on battery)"
			print(f" * AC status: {self.color(on_ac, out)}")
			print(f" * Ignore inhibit: {powerbus.model.ignore_inhibit}")
			sleep_inhibit = await sleep_inhibited()
			session_inhibit, inhibitors = self.session_sleep_inhibited()
			print(f" * Sleep inhibited (system) :", self.color(sleep_inhibit))
			print(f" * Sleep inhibited (session):", self.color(session_inhibit))
			if session_inhibit:
				for client_key, inhibitor_dict in inhibitors.items():
					print(f"   > {self.color(client_key)}")
					for app_name, extras in inhibitor_dict.items():
						print(f"     \\ {app_name} : {extras}")
			print(colorama.Style.RESET_ALL)
			await asyncio.sleep(5)

	async def on_recv(self, ws, msg_str):
		msg_obj = powerbus.socket.PowerBusMessage.from_msg(msg_str)
		for req_key in ["USER", "DISPLAY", "time", "idle", "inhibitors"]:
			if msg_obj.get(req_key, None) is None:
				logging.warning(f"Received invalid message! Missing: {req_key}")
				return

		msg_time = msg_obj.time
		cur_time = get_utc_time()

		sys.stdout.write(".")
		sys.stdout.flush()

		if msg_time > cur_time:
			logging.warning("message from FUTURE!")
			return
		elif cur_time - msg_time > self.stale_msg_interval:
			logging.warning("OLD message!")
			return

		client_key = set()
		for key in ["USER", "DISPLAY"]:
			client_key.add((key, msg_obj[key]))

		self.clients[client_key_from_msg(msg_obj)] = (ws, msg_obj)

	def remove_client(self, ws):
		"""
		Remove active client connection identified by live WebSocket object.
		"""
		client_key = None
		for cur_client, datums in self.clients.items():
			if id(datums[0]) == id(ws):
				client_key = cur_client
				break
		if client_key:
			del self.clients[client_key]


def client_key_from_msg(msg_obj):
	return f"{msg_obj['USER']}{msg_obj['DISPLAY']}"


def get_utc_time():
	# pymongo's BSON decoding gives us a timestamp with a timezone, so we need ours to have one too:
	return datetime.now(timezone.utc)
