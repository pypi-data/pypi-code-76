from __future__ import absolute_import
import os
import logging
import importlib
import mbed_lstools
from mcutk.debugger.general import DebuggerBase
from mcutk.pserial.serial import Serial


def getboard(name, **kwargs):
    """An entry to get board instance.

    Arguments:
        name {string} -- board name
    """
    devicename = kwargs.pop("devicename", "")
    try:
        boardmodule_path = "mcutk.board.%s"%name
        logging.debug(boardmodule_path)
        boardmodule = importlib.import_module(boardmodule_path)
        board = boardmodule.Board(devicename, **kwargs)
    except ImportError as e:
        board = Board(devicename, **kwargs)

    logging.debug(str(board))
    board.name = name
    return board




class Board(object):
    """MCUTK base board. Defined common interface & functions.
    This object can be used directly and provide general support for Kinetis series.
    """
    def __init__(self, devicename=None, **kwargs):
        """Create a mcutk.Board instance.

        Arguments:
            devicename {string} -- device name
            interface {string} -- SWD/JTAG

        Keyword Arguments:
            debugger_type {string} -- debugger type, choices are defined in
        """
        self.name = kwargs.get('name', '')
        self.devicename = devicename
        self._debugger = None
        self._serial_ports = list()

        self.interface = kwargs.get("interface", "SWD")
        self.debugger_type = kwargs.get("debugger_type", "jlink")

        # default gdbport is 3000
        self.gdbport = kwargs.get("gdbport", 3333)
        self.usbid = kwargs.get("usbid")
        self.serial = kwargs.get("serial", "")
        self.baudrate = kwargs.get("baudrate", "115200")
        self.start_address = kwargs.get("start_address", "0")

        self.sp = None #"(0x00000000)"
        self.pc = None #"(0x00000004)"
        self.resource = []

    def __repr__(self):
        return "<{0}(name={1.devicename}, usbid={1.usbid})>".format(self.__class__.__name__, self)

    def get_mount_point(self):
        """Return mount point by matching usbid.
        """
        mbeds = mbed_lstools.create()
        mbeds_devices = mbeds.list_mbeds(filter_function=lambda m: m["target_id"] in self.usbid)
        if not mbeds_devices:
            return
        return mbeds_devices[0]['mount_point']

    def set_serial(self, port, baudrate, **kwargs):
        """Set or add serial port to board object, this interface will pass all
        parameters to serial.Serial object. For more details, please refer to pyserial
        documentation: https://pythonhosted.org/pyserial/pyserial_api.html#classes.

        Default timeout=1.
        """
        if not port:
            return None
        timeout = kwargs.pop('timeout', 1)
        sp = Serial(timeout=timeout, **kwargs)
        sp.port = port
        sp.baudrate = baudrate
        self._serial_ports.append(sp)

    def get_serial(self, index=0):
        """Get serial port instance by index.
            0 -- main
            1 -- secondary
            2 -- third

        Arguments:
            index {int} -- the port index.

        Returns:
            pyserial, serila.Serial instance,
        """
        if not self._serial_ports:
            logging.debug('no serial ports are configured!')
            return None

        try:
            return self._serial_ports[index]
        except IndexError:
            return None

    def remove_resource(self, res_inst):
        for res in self.resource:
            if id(res[1]) == id(res_inst):
                logging.warning("find resource for %s", id(res_inst))
                self.resource.remove(res)

        logging.warning("resource for %s not found", id(res_inst))
        return None

    def register_resource(self, res_inst, naming):
        """
        regist resources to board
        res_init: resource instance
        naming: name string of this resource
        """
        res = [naming, res_inst]

        self.resource.insert(-1, res)

    def find_resource_by_name(self, naming):
        """
        find a resource by name
        naming: the name of the resource
        return: the first match resource or None
        """
        for res in self.resource:
            if res[0] == naming:
                return res[1]

        logging.debug("resource for %s not found", naming)
        return None

    def find_resource_by_type(self, type_string):
        """
        find a resource by type
        type_string: the name of resource type(class)
        return: a list of matched resource, otherwise None
        """
        ret = []
        for res in self.resource:
            if type(res[1]).__name__ == type_string:
                logging.info("find resource for %s", type_string)
                ret.insert(-1, res[1])

        logging.info("resource for %s not found", type_string)
        return None

    @property
    def debugger(self):
        if self._debugger:
            self._debugger.set_board(self)
        return self._debugger

    @debugger.setter
    def debugger(self, value):
        if not value:
            return
        if isinstance(value, DebuggerBase):
            self._debugger = value
        else:
            ValueError("This not a valid debugger object")

    @property
    def gdb_init_commands(self):
        """gdb.init is a string include gdb commands.

        It will be rendered before execute 'gdb -x gdb.init'.
        Default it is loaded from debugger.gdbinit_template.
        Overwrite this function can custom the commands.
        """
        return None

    @property
    def ser_main(self):
        """A shortcut attribute to access the main serial port object.
        """
        return self.get_serial(0)

    @property
    def ser_sec(self):
        """A shortcut attribute to access the secondary serial port object.
        """
        return self.get_serial(1)

    def reset_board_by_send_break(self, serial=None):
        """CMSIS-DAP firmware allows the target to be reset by sending a break command
        over the serial port.
        Default use the main serial port.
        """
        if serial == None:
            serial = self.ser_main

        logging.info('reset board by sending break to port: %s', serial.port)
        _opened_by_me = False
        if not serial.is_open:
            _opened_by_me = True
            serial.open()

        try:
            serial.send_break()
        except:
            serial.break_condition = False

        # if port status is aligned with the origin.
        if _opened_by_me:
            serial.close()

        return True

    def reset(self, method="debugger"):
        """Reset board. There are several methos allow user to reset board.
        By default it is debugger method.

        Reset method list:
            - debugger: use debugger(JTAG) to reset board
            - serial: send break via serial port

        Keyword Arguments:
            method {str} -- [description] (default: {"debugger"})
        """
        if method == 'serial':
            return self.reset_board_by_send_break()

        elif method == "debugger":
            assert self.debugger
            return self.debugger.reset()

        else:
            raise ValueError('unknow reset method %s'%method)

    def programming(self, filename, **kwargs):
        """Auto program binary to board.

        For general situation, it is avaliable for most boards.
        It will choose gdb or general method by filename extension.

        params:
            filename: path to image file.
        """
        version = self.debugger.version if self.debugger.version else 'unkown'
        logging.info("%s, debugger=%s, version=%s", self.name, self.debugger_type, version)
        logging.info("programming %s", filename)
        ext = os.path.splitext(filename)[-1]
        if self.debugger_type in ("jlink", "pyocd"):
            if ext in (".bin", ".img"):
                return self.debugger.flash(filename, addr=self.start_address)
            else:
                return self.debugger.gdb_program(filename, **kwargs)
        else:
            return self.debugger.flash(filename, **kwargs)

    def check_serial(self):
        """Check serial port.
        """
        status = "pass"
        try:
            self.ser_main.write_timeout = 2
            self.ser_main.open()
        except Exception as e:
            status = str(e)
        finally:
            if self.ser_main and self.ser_main.is_open:
                self.ser_main.close()

        return status
