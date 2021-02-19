from __future__ import absolute_import
import os
import logging
from distutils.version import LooseVersion

# pyocd version >= 0.13
from pyocd import __version__ as pyocd_version
from pyocd.target import TARGET
from pyocd.core.helpers import ConnectHelper
try:
    from pyocd.flash.file_programmer import FileProgrammer
except ImportError:
    from pyocd.flash.loader import FileProgrammer

from pyocd.probe import aggregator
from pyocd.probe.cmsis_dap_probe import CMSISDAPProbe

# CMSIS DAP only due to https://github.com/mbedmicro/pyOCD/issues/877
if isinstance(aggregator.PROBE_CLASSES, list):
    aggregator.PROBE_CLASSES = [
        CMSISDAPProbe
    ]

from mcutk.debugger.general import DebuggerBase
from mcutk.util import run_command

logging.getLogger('pyocd.flash.loader').setLevel(logging.INFO)
logging.getLogger('pyocd.coresight.rom_table').setLevel(logging.WARNING)

class PYOCD(DebuggerBase):
    """
    Wrap pyOCD to a standard debugger for pymcutk.

    pyOCD is an open source Python package for programming and debugging Arm Cortex-M
    microcontrollers using multiple supported types of USB debug probes. It is fully
    cross-platform, with support for Linux, macOS, and Windows.

    For more visit https://github.com/mbedmicro/pyOCD.
    """

    def __init__(self, **kwargs):
        super(PYOCD, self).__init__("pyocd", ".", **kwargs)
        self.target_override = None
        self.version = pyocd_version
        self.loose_version = LooseVersion(self.version) if self.version else LooseVersion("0.1")

    @property
    def is_ready(self):
        return self.version not in (None, '')

    def set_board(self, board):
        # workaround to clear the prefix of usbid
        if board.usbid and ":" in board.usbid:
            board.usbid = board.usbid.split(":")[-1]
        self._board = board
        self._check_overried_target(board.devicename)

    def get_session(self, **kwargs):
        """Return a pyocd Session."""
        if kwargs.get('auto_open') == False:
            kwargs['auto_open'] = False
            kwargs['open_session'] = False

        return ConnectHelper.session_with_chosen_probe(
            blocking=False,
            unique_id=self._board.usbid,
            target_override=self.target_override,
            **kwargs
            )

    def _check_overried_target(self, devicename):
        """Overried target if device name is include in pyOCD.target.TARGET.
        This is very useful if you want to use other device target for debugging.
        """
        if devicename.endswith('pack') and os.path.exists(devicename):
            self.target_override = devicename

        elif self.is_ready and devicename in TARGET:
            self.target_override = devicename

    def _get_default_session_options(self):
        """ pyocd support to config options to control
        pyocd behaviour. Guide: https://github.com/mbedmicro/pyOCD/blob/master/docs/options.md
        """
        options = {}
        # pyocd 0.23: pre_reset to deal with low power mode
        if self.loose_version >= LooseVersion("0.23.0"):
            if self._board and not self._board.name.startswith("evk"):
                # workaround for none kinetis series
                options['connect_mode'] = 'under-reset'

        # pyocd 0.25: support allow_no_cores
        if self.loose_version >= LooseVersion("0.25.0"):
            options['allow_no_cores'] = True

        return options

    def _build_cmd_args(self, board=None, options=None):
        """Build command line arguments."""
        if not board:
            board = self._board

        if not options:
            options = self._get_default_session_options()

        args = list()
        if board:
            if self.loose_version < LooseVersion("0.13.0"):
                args.append("-b %s" % board.usbid)
            else:
                args.append("-u %s" % board.usbid)

        if self.target_override:
            if self.target_override.endswith('.pack'):
                args.append('--pack %s' % self.target_override)
            else:
                args.append('-t %s' % self.target_override)

        if options:
            for item in options.items():
                args.append("-O %s=%s" % (item[0], str(item[1]).lower()))

        return " ".join(args)

    def list_connected_devices(self):
        """List connected CMSIS-DAP devices."""

        probes = ConnectHelper.get_all_connected_probes(blocking=False)
        devices = list()
        for probe in probes:
            device = {
                'usbid': probe.unique_id,
                'name': probe.description,
                'type': 'pyocd'
            }
            devices.append(device)
        return devices

    def test_conn(self):
        """Test debugger connection."""

        if self._board is None:
            raise ValueError("board is not set")

        msg = "NoError"
        try:
            with self.get_session():
                pass
        except Exception as err:
            msg = "ConnectError: %s" % str(err)

        return msg

    def read32(self, addr):
        with self.get_session(options={'connect_mode': 'attach'}) as session:
            return session.board.target.read_memory(addr)

    def write32(self, addr, value):
        with self.get_session(options={'connect_mode': 'attach'}) as session:
            session.board.target.write_memory(addr, value)

    def erase(self, **kwargs):
        """Mass erase flash."""

        if self.loose_version >= LooseVersion("0.25.0") or 'dev' in self.version:
            command = "pyocd erase --mass -v --no-wait"
        else:
            command = "pyocd erase --mass-erase -v"

        command += " " + self._build_cmd_args(options={
            "resume_on_disconnect": False,

        })
        logging.info(command)
        return run_command(command, timeout=120)[0]

    def reset(self):
        """Always perform a hardware reset"""

        logging.info("resetting board by pyocd")
        # do not auto open probe by session it self, because we do not need to
        # init target and flash. Just use probe to perform a hardware reset.
        # This can improve the stability even if board is in lower mode.
        session = self.get_session(auto_open=False)
        if not session:
            logging.error("cannot create session with probe id: %s", self._board.usbid)
            return False

        try:
            session.probe.open()
            session.probe.set_clock(1000000)
            session.probe.connect()
            session.probe.reset()
            session.probe.disconnect()
        finally:
            session.probe.close()
        logging.info("reset done.")
        return True

    def unlock(self):
        """Unlock board."""

        logging.info("unlock board")
        try:
            with self.get_session(options={'auto_unlock': True}):
                pass
            return True
        except:
            logging.exception("exception")
            return False

    def get_gdbserver(self, **kwargs):
        """Return gdb server command. If configured board.devicename is a target
        name in pyocd.target.TARGET. This will overried the target.
        """

        board = kwargs.get('board')
        port = kwargs.get('port')

        if board is None:
            board = self._board

        if board:
            port = board.gdbport

        if self.loose_version >= LooseVersion("0.13.0"):
            command = "pyocd gdbserver --no-wait" # --trust-crc
            if port:
                command += " --port %s" % port
        else:
            # compatible with old version of pyocd
            command = "pyocd-gdbserver"
            if port:
                command += " -p %s" % port

        if kwargs.get('erase'):
            command += " --erase %s" % kwargs.get("erase")

        if kwargs.get("script"):
            command += " --script %s" % kwargs.get("script")

        if kwargs.get("core") and self.loose_version >= LooseVersion("0.27.0"):
            command += " --core %s" % kwargs.get("core")

        options = self._get_default_session_options()
        # set console to disable telent server
        if self.loose_version >= LooseVersion("0.23.0"):
            options['semihost_console_type'] = 'console'
            options['keep_unwritten'] = 'false'

        command += " " + self._build_cmd_args(board, options)
        return command

    def flash(self, filepath, **kwargs):
        """Flash chip with filepath. (bin, hex).

        Arguments:
            erase: erase chip yes or not.
            addr: being the integer starting address for the bin file.
        """
        addr = kwargs.get('addr')
        filepath = filepath.replace("/", "/")
        options = self._get_default_session_options()
        session = self.get_session(options=options)
        if session is None:
            raise ValueError("No device available to flash")

        file_format = 'elf'
        if filepath.endswith(".bin"):
            file_format = 'bin'
        elif filepath.endswith('.hex'):
            file_format = 'hex'

        with session:
            # call registerd callback function
            self._call_registered_callback("before_load")
            programmer = FileProgrammer(session, trust_crc=True)
            programmer.program(filepath, file_format)
        return 0, ''

    def gdb_init_template(self):
        """Return default pypcd gdb commands."""
        commands = [
            "set remotetimeout 10",
            "target remote localhost:{gdbport}",
            # imxrt series, safe to reset and halt chip
            # pyocd version < 0.28, the monitor reset will do reset_and_halt
            # but when version >= 0.28, reset just reset core without halt
            # to compatible with old version, we reset twice.
            # It's safe to remove "monitor reset" in future if we deprecated
            # pyocd < 0.28
            "monitor reset --halt" if self.loose_version > LooseVersion("0.27.3") else "monitor reset",
            "monitor halt",
            "load",
        ]

        if self._board and self._board.sp:
            commands.append("x {sp}")
            commands.append("set $sp=$__")

        if self._board and self._board.pc:
            commands.append("x {pc}")
            commands.append("set $pc=$__")

        commands.append("q")
        return "\n".join(commands)

    def __str__(self):
        return "pyocd-%s" % self.version

    @staticmethod
    def get_latest():
        debugger = PYOCD()
        return debugger if debugger.is_ready else None
