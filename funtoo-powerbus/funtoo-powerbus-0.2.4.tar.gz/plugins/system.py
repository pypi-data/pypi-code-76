#!/usr/bin/env python3

import asyncio
import logging
import os
import subprocess
import sys
from datetime import datetime, timezone, timedelta

import colorama
import zmq.asyncio
from dbus_next import Message, BusType
from dbus_next.aio import MessageBus

from subpop.hub import DeferredHubProperty

LID_CLOSED_EVENT = asyncio.Event()
LID_LAST_CLOSED = None
LID_LAST_OPENED = None

import dyne.org.funtoo.powerbus as powerbus


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
				print(str(my_dict["LidIsClosed"]))
				logging.warning("Lid is closed!")
				LID_LAST_CLOSED = datetime.utcnow()
				LID_CLOSED_EVENT.set()
				LID_CLOSED_EVENT.clear()
			else:
				LID_LAST_OPENED = datetime.utcnow()

	bus_name = "org.freedesktop.UPower"
	path = "/" + bus_name.replace(".", "/")
	introspection = await bus.introspect(bus_name, path)
	obj = bus.get_proxy_object(bus_name, path, introspection)
	props = obj.get_interface("org.freedesktop.DBus.Properties")
	props.on_properties_changed(upower_callback)


class PowerBusDaemon(object):
	def __init__(self):

		if not self.is_root:
			raise PermissionError()

		if not os.path.isdir("/run"):
			raise FileNotFoundError("/run not found and required by funtoo-powerbus.")
		os.umask(0o022)
		if not os.path.exists("/run/funtoo"):
			os.mkdir("/run/funtoo", 0o700)

		# Give us exclusive access to this directory while we set it up:
		os.chown("/run/funtoo", 0, 0)
		os.chmod("/run/funtoo", 0o700)
		try:
			put_file("/run/funtoo/powerbus.pid", str(os.getpid()))
		except PermissionError:
			raise PermissionError("Unable to write PID file at /runt/funtoo/powerbus.pid.")

		os.umask(0o000)
		# ZMQ Setup:
		self.bind_addr = powerbus.zmq_bus.BUS_PATH
		self.ctx = zmq.asyncio.Context()
		self.identities = {}
		self.server: zmq.asyncio.Socket = self.ctx.socket(zmq.ROUTER)
		self.server.bind(self.bind_addr)

		# Now that all files (including powerbus-socket) are in place -- relax permissions.
		os.chmod("/run/funtoo", 0o755)
		os.umask(0o022)
		logging.debug(f"Listening for new client connections at {self.bind_addr}")

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

	@property
	def is_root(self):
		return os.geteuid() == 0

	def go_to_sleep(self):
		subprocess.getoutput("echo -n mem > /sys/power/state")

	async def send_message_to_all_active_clients(self, msg_obj: powerbus.zmq_bus.PowerBusMessage):
		print("Going to possibly send messages...")
		cur_time = get_utc_time()
		for client_key, orig_msg_obj in self.clients.items():
			if cur_time - orig_msg_obj.time <= self.client_stale_timeout:
				print("Sending message", msg_obj)
				await msg_obj.send(self.server, identity=orig_msg_obj.identity)

	async def tell_clients_to_prepare_for_sleep(self):
		msg_obj = powerbus.zmq_bus.PowerBusMessage(action="prepare-for-sleep")
		await self.send_message_to_all_active_clients(msg_obj)

	@property
	def num_clients(self):
		num_fresh_clients = 0
		cur_time = get_utc_time()
		for client_key, msg_obj in self.clients.items():
			if cur_time - msg_obj.time <= self.client_stale_timeout:
				num_fresh_clients += 1
		return num_fresh_clients

	def sufficiently_idle(self, timeout_ms):

		"""
		This method will look at all non-stale clients connected, and look at their idle times. If there is at least
		one actively communicating client, and all clients' idle times are greater than ``self.idle_sec``, then we
		have passed our first test in determining if we should sleep, and we will return True. Otherwise, this method
		will return False.

		This doesn't mean we will definitely go to sleep, because sleep could be inhibited via logind. But we can now
		proceed to see if it's bed time.

		:return: Whether or not the system is sufficiently idle to go to sleep.
		:rtype: bool
		"""
		num_fresh_clients = 0
		num_idle_clients = 0
		cur_time = get_utc_time()
		for client_key, msg_obj in self.clients.items():
			if cur_time - msg_obj.time <= self.client_stale_timeout:
				num_fresh_clients += 1
				if msg_obj.idle > timeout_ms:
					num_idle_clients += 1

		if num_fresh_clients > 0 and num_idle_clients == num_fresh_clients:
			return True
		else:
			return False

	def session_sleep_inhibited(self):
		user_inhibited = {}
		for client_key, msg_obj in self.clients.items():
			if len(msg_obj.inhibitors):
				user_inhibited[client_key] = msg_obj.inhibitors
		return len(user_inhibited) > 0, user_inhibited

	async def start(self):
		await hub.add_property("SYSTEM_BUS", DeferredHubProperty(lambda: MessageBus(bus_type=BusType.SYSTEM).connect()))
		self.has_lid = await get_upower_property("lid_is_present")
		if self.has_lid:
			await setup_lid_callback()
		asyncio.create_task(self.sleep_handler())
		asyncio.create_task(self.lid_event_monitor_task())
		asyncio.create_task(self.status_display())
		asyncio.create_task(self.stale_cleanup_task())
		while True:
			msg = await self.server.recv_multipart()
			self.on_recv(msg)

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
			for client_key, msg_obj in self.clients.items():
				if cur_time - msg_obj.time > self.client_stale_timeout:
					continue
				new_clients[client_key] = msg_obj
			self.clients = new_clients

	async def lid_event_monitor_task(self):

		# TODO: right now, we just ignore handling the lid close event if we are on AC power. But an advanced
		#       feature we might want is the option to go to sleep if lid is closed with NO EXTERNAL DISPLAYS
		#       and we are on AC power. But I don't think that's needed for 1.0.

		while True:
			await LID_CLOSED_EVENT.wait()
			if not on_ac_power():
				self.last_maybe_accelerated_sleep = datetime.utcnow()
				self.lid_closed_accelerated_sleep = True

	async def sleep_handler(self):
		"""
		This method actually sees if we should go to sleep -- now -- and if so, will put the system to sleep.
		It contains the important logic for determining this, all in one central place. This is one of the
		important goals of powerbus -- to have all this logic in one place where it can be easily understood,
		and modified or enhanced if desired.
		"""
		while True:
			await self.send_message_to_all_active_clients(powerbus.zmq_bus.PowerBusMessage({"action": "ping"}))
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
				# let's really make sure the lid is still closed, and if it's not, let's not try to sleep very soon!
				if await lid_is_closed():
					# OK, lid is really closed -- so we will try to go to sleep very soon.
					timeout_ms = self.lid_closed_idle_delay_ms
				else:
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
				# We are about to sleep, and this is an "accelerated" sleep due to the lid being closed.
				# Therefore, update the timestamp for the last accelerated sleep, and also turn off accel.
				# sleep mode -- it can only be active for one shot, then it gets disabled until the lid is
				# closed again.
				self.last_accelerated_sleep = datetime.utcnow()
				self.lid_closed_accelerated_sleep = False
			else:
				self.last_sleep_attempt = datetime.utcnow()

			await self.tell_clients_to_prepare_for_sleep()
			await asyncio.sleep(0.25)
			self.go_to_sleep()

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
					print(f"   > {self.color(client_key_to_str(client_key))}")
					for app_name, extras in inhibitor_dict.items():
						print(f"     \\ {app_name} : {extras}")
			print(colorama.Style.RESET_ALL)
			await asyncio.sleep(2)

	def on_recv(self, msg):
		# First, receive and inspect message:
		zmq_identity = msg[0]
		logging.info("Received: %s" % msg)
		msg_obj = powerbus.zmq_bus.PowerBusMessage.from_msg(msg[1])
		msg_time = msg_obj.time
		cur_time = get_utc_time()

		sys.stdout.write(".")
		sys.stdout.flush()

		if msg_time > cur_time:
			print("message from FUTURE!")
			return
		elif cur_time - msg_time > self.stale_msg_interval:
			print("OLD message!")
			return

		existing_keys = ["USER", "DISPLAY"]
		client_key = set()
		for key in existing_keys:
			if key in msg_obj:
				client_key.add((key, msg_obj[key]))
		# Record identity for sending messages back:
		msg_obj.identity = zmq_identity

		self.clients[frozenset(client_key)] = msg_obj


def client_key_to_str(client_key):
	t = {}
	for key, val in client_key:
		t[key] = val
	return f"{t['USER']}{t['DISPLAY']}"


def get_utc_time():
	# pymongo's BSON decoding gives us a timestamp with a timezone, so we need ours to have one too:
	return datetime.now(timezone.utc)
