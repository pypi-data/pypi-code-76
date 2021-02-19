import sys
import os
import time
import logging
import subprocess
import threading
import socket
import errno
import shlex
from contextlib import closing

import mbed_lstools
from pexpect.popen_spawn import PopenSpawn
from mcutk.appbase import APPBase
from mcutk.gdb_session import GDBSession
from mcutk.exceptions import GDBServerStartupError

PY = sys.version_info[0]


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

class DebuggerBase(APPBase):
    """A general debugger class to define basic debugger interfaces.

    All debugger should instantiat from this class.
    """
    STAGES = ['before_load']

    def __init__(self, *args, **kwargs):
        super(DebuggerBase, self).__init__(*args, **kwargs)
        self.gdbpath = kwargs.get("gdbpath", "")
        self.version = kwargs.get("version", "unknown")
        self._board = None
        self._callback_map = {
            "before_load": None
        }

    def __str__(self):
        return "<Debugger: name={}, version={}>".format(self.name, self.version)

    @property
    def is_ready(self):
        return True

    def set_board(self, board):
        self._board = board

    def gdb_init_template(self):
        """Return a string about gdb init template.
        """
        return ""

    def reset(self):
        """Used to reset target CPU.
        """
        pass

    def erase(self, **kwargs):
        """Used to erase flash.
        """
        pass

    def flash(self, filepath, **kwargs):
        """Binary image programming.
            .bin
            .hex
        """
        pass

    def get_gdbserver(self, **kwargs):
        """Return a string about the command line of gdbserver
        """
        raise NotImplementedError("not support")

    def read32(self, addr):
        """read a 32-bit word"""
        raise NotImplementedError("not support")

    def write32(self, addr, value):
        """write a 32-bit word"""
        raise NotImplementedError("not support")

    def start_gdbserver(self, **kwargs):
        gdbserver_cmd = self.get_gdbserver(**kwargs)
        print(gdbserver_cmd)
        # start gdb server
        subprocess.call(gdbserver_cmd, shell=True)

    def list_connected_devices(self):
        mbeds = mbed_lstools.create()
        devices = mbeds.list_mbeds()
        for device in devices:
            device['usbid'] = device.pop('target_id_usb_id')
            device['type'] = device.pop('device_type')
            device['name'] = device.pop('platform_name')
            if device['type'] == 'daplink':
                device['debugger'] = 'pyocd'

        return devices

    def gdb_program(self,
                    filename,
                    gdbserver_cmdline=None,
                    gdbinit_commands=None,
                    board=None,
                    timeout=200,
                    **kwargs):
        """Using gdb & gdbserver to programming image.
        Steps:
            1> Start gdbserver at port: board.gdbport
            2> Render gdbinit_template
            3> Start gdb.exe:
                gdb.exe -x <gdb.init> -se <binary.file>

        Arguments:
            filename - {str}: path to image file.
            gdbserver_cmdline - {str}: gdb server command line, used for starting gdb server.
            gdbinit_commands - {str}: gdb init commands to control gdb behaviour.
            timeout - {int}: set timeout for gdb & gdb server process. default 200 seconds.

        Returns:
            tuple --- (returncode, console-output)
        """
        timer = None
        try:
            session, timer, server_output = self._start_gdb_session(
                filename,
                gdbserver_cmdline,
                gdbinit_commands,
                board,
                timeout,
                **kwargs)
            if not session:
                return 1, server_output

            # gdb client disconnect the connection,
            # and gdbsever will automaticlly close
            session.close()
            session.gdb_server_proc.wait()
        except GDBServerStartupError:
            return 1, ""

        finally:
            # Stop timeout timer when communicate call returns.
            if timeout is not None and timer:
                timer.cancel()

        logging.info("gdbserver exit code: %s", session.gdb_server_proc.returncode)

        # get gdb console output
        output = server_output
        output += session.console_output
        retcode = session.gdb_server_proc.returncode
        return retcode, output

    def _start_gdb_session(self,
                           filename,
                           gdbserver_cmdline=None,
                           gdbinit_commands=None,
                           board=None,
                           timeout=None,
                           **kwargs):
        """Return a attached gdb session object"""

        if board is None:
            board = self._board

        if not self.gdbpath:
            raise IOError("Invalid gdb executable")

        if board is None:
            raise ValueError('no board is associated with debugger!')

        timer = None
        gdb_errorcode = 0
        if os.name != "nt" or not board.gdbport:
            # On Linux, port cannot be released even if current process
            # is terminted, to avoid exception "Address already in use";
            # Find and use free port from socket.
            board.gdbport = find_free_port()

        if not gdbinit_commands:
            # load gdb init template
            gdb_cmds_template = board.gdb_init_commands if board.gdb_init_commands \
                                else self.gdb_init_template()
        else:
            gdb_cmds_template = gdbinit_commands

        gdbcommands = render_gdbinit(gdb_cmds_template, board)
        gdbserver_cmd = gdbserver_cmdline if gdbserver_cmdline else self.get_gdbserver(**kwargs)
        logging.info("gdbserver: %s", gdbserver_cmd)

        # start gdb server
        if os.name != "nt":
            gdbserver_cmd = shlex.split(gdbserver_cmd)

        start = time.time()
        gdbserver_proc = subprocess.Popen(
            gdbserver_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=False)

        time.sleep(0.5)
        if os.name == "nt" and not _validate_port_is_ready(gdbserver_proc, board.gdbport):
            if gdbserver_proc.poll() is None:
                gdbserver_proc.kill()
            output, _ = gdbserver_proc.communicate()
            logging.error(">>> gdbserver start failure, console output: \n\n%s", output)
            raise GDBServerStartupError("gdb server start failure")

        logging.info("gdbserver is ready, pid: %s, port: %s.", gdbserver_proc.pid, board.gdbport)
        server_output = list()

        def stdout_reader(process):
            for line in iter(process.stdout.readline, b''):
                if process.poll() != None:
                    break
                if PY > 2:
                    line = line.decode("utf-8", 'ignore')
                server_output.append(line)

        # To resolve large output from subprocess PIPE, use a background thread to continues read
        # data from stdout.
        reader_thread = threading.Thread(target=stdout_reader, args=(gdbserver_proc, ))
        reader_thread.start()

        # start gdb client
        output = ""
        logging.info("start gdb client to connect to server.")
        gdb_cmd = '{} --exec {} --silent -ex "set tcp auto-retry on" -ex "set tcp connect-timeout 30"'.format(self.gdbpath, filename)
        session = GDBSession.start(gdb_cmd)
        session.gdb_server_proc = gdbserver_proc

        # set timeout
        # Use a timer to stop the subprocess if the timeout is exceeded.
        if timeout is not None:
            session.timeout = timeout
            ps_list = [gdbserver_proc, session]
            timer = threading.Timer(timeout, timeout_exceeded, (ps_list, ))
            timer.start()

        # convert string commands to a list
        _gdb_actions = [line.strip() for line in gdbcommands.split("\n") if line.strip()]

        # remove q command
        if 'q' in _gdb_actions:
            _gdb_actions.remove("q")

        for act in _gdb_actions:
            # call registerd callback function before_load command
            if act.startswith("load"):
                self._call_registered_callback("before_load")
            try:
                c = session.run_cmd(act)
                if "No connection could be made" in c or "Target disconnected" in c\
                    or "Connection timed out" in c or '"monitor" command not supported by this target' in c \
                    or "Error finishing flash operation" in c or "Load failed" in c:
                    gdb_errorcode = 1
                    logging.error(c)
                    break
            except:
                logging.exception('gdb cmd error, CMD: %s', act)
                gdb_errorcode = 1

        if gdb_errorcode == 1:
            session.close()
            session = None
            try:
                gdbserver_proc.terminate()
                reader_thread.join()
            except:
                pass

        print("time used: %s" % (time.time() - start))
        return session, timer, "".join(server_output)


    def start_gdb_debug_session(self,
                                filename,
                                gdbserver_cmdline=None,
                                gdbinit_commands=None,
                                board=None,
                                **kwargs):
        """Return a attached gdb session object"""
        session, _, _ = self._start_gdb_session(
            filename, gdbserver_cmdline, gdbinit_commands,
            board, timeout=None, **kwargs)

        return session

    def register(self, name):
        """Declare a decorator to register callback to debugger instance.

        Arguments:
            name {str} -- before_load
        """
        def func_wrapper(func, *args, **kwagrs):
            self._callback_map[name] = (func, args, kwagrs)
            return func
        return func_wrapper

    def register_callback(self, stage, func, *args, **kwagrs):
        assert stage in DebuggerBase.STAGES
        self._callback_map[stage] = (func, args, kwagrs)

    def remove_callback(self, stage):
        if stage in self._callback_map:
            del self._callback_map[stage]

    def _call_registered_callback(self, name=None):
        value = self._callback_map.get(name)
        if type(value) is tuple:
            func, args, kwargs = value
            if func:
                return func(*args, **kwargs)
        return None

def timeout_exceeded(ps):
    """subprocess tiemout exceeded handler."""
    # process.kill() just killed the parent process, and cannot kill the child process
    # that caused the popen process in running state.
    # force to use windows command to kill that the process!
    for process in ps:
        proc = process
        if isinstance(process, PopenSpawn):
            proc = process.proc

        logging.warning('pid: %s exceeded timeout, force killed', proc.pid)
        if os.name == "nt":
            os.system("TASKKILL /F /PID {pid} /T".format(pid=proc.pid))
        else:
            process.kill()


def render_gdbinit(template, board):
    """
    Render gdbinit template with board object.

    Render used '.foramt()' syntax:
        'target remote localhost: {gdbport}'

    Example:
        1. jlink
    """
    if board.debugger_type == 'pyocd':
        if board.sp:
            board.sp = board.sp.replace("(", "").replace(")", '')
        if board.pc:
            board.pc = board.pc.replace("(", "").replace(")", '')
    dicta = board.__dict__
    # dicta["file"] = executable
    return template.format(**dicta)


def _validate_port_is_ready(server_process, port, tiemout=50):
    """Validate the port is open on localhost"""

    is_ready = False
    port = int(port)
    s = None

    assert server_process != None

    for _ in range(tiemout):
        print(" Wait for gdb server ready.")
        time.sleep(0.5)
        if server_process.poll() is None:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.bind(("127.0.0.1", port))
            except socket.error as e:
                if e.errno == errno.EADDRINUSE:
                    is_ready = True
                    break
                else:
                    print(e)
            finally:
                if s is not None:
                    s.close()
        else:
            break

    return is_ready
