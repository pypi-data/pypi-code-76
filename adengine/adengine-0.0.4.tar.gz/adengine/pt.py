import subprocess
import json
import time
import platform
import os
import socket
import typing
import logging
import datetime
import re
import signal
import pathlib

logger = logging.getLogger('adengine.pt')

__all__ = [
    'PacketTracerSession',
    'extract_data',

    'PacketTracerSessionError',
    'PacketTracerSessionNotStarted',
    'PacketTracerSessionAlreadyRunning',

    'LaunchingPacketTracerError',
    'LaunchingPacketTracerTimeout',

    'ExtractorError',
    'GeneralError',
    'WrongCredentials',
    'ConnectionFailed',
    'ArgumentsParsingError',
    'ActivityFileReadingError',
    'ActivityNeedsPassword',
    'TopologyFilesNotSupported',
    'WrongPassword',
]

if 'PT7HOME' in os.environ:
    PT_HOME = os.environ['PT7HOME']
    PT_EXECUTABLE_NAME = 'PacketTracer7'
elif 'PT8HOME' in os.environ:
    PT_HOME = os.environ['PT8HOME']
    PT_EXECUTABLE_NAME = 'PacketTracer'
else:
    raise Exception('PacketTracer is not installed')

PT_BIN_ROOT = os.path.join(PT_HOME, 'bin')
PT_EXECUTABLE = os.path.join(PT_BIN_ROOT, PT_EXECUTABLE_NAME)


def _get_ade_path():
    possible_ade_paths = [
        os.path.join(PT_HOME, 'extensions/ade/ade.jar'),
        os.path.join(pathlib.Path().home(), 'extensions/ade/ade.jar'),
    ]
    for ade_path in possible_ade_paths:
        if os.path.exists(ade_path):
            return ade_path

    raise Exception('Activity Data Extractor is not installed')


ADE = _get_ade_path()


def _check_java_version():
    """Checks java version.

    If Java version 8 or newer, do nothing, else, raises Exception.

    Raises:
        Exception: when java version older than 8
    """
    java_ver_result = subprocess.run(['java', '-version'],
                                     text=True,
                                     capture_output=True)
    if java_ver_result.returncode:
        raise Exception('Java not installed. Please install Java 8 or newer.')
    else:
        java_ver = re.search('[0-9]+\.[0-9]+\.[0-9_+]+', java_ver_result.stderr.split('\n')[0]).group(0)
        java_ver = java_ver.split('.')
        if not (int(java_ver[0]) >= 9 or (java_ver[0] == '1' and java_ver[1] == '8')):
            raise Exception(f'Installed Java is too old: {".".join(java_ver)}. Please install Java 8 or newer.')


_check_java_version()


class LaunchingPacketTracerError(Exception):
    """This exception is used to indicate that Packet Tracer stated with error"""

    def __init__(self, port: int, nogui: bool):
        super().__init__()
        self._port = port
        self._nogui = nogui

    def __str__(self):
        return f'An error occurred while launching Packet Tracer on port {self._port} with nogui={self._nogui}'

    @property
    def port(self) -> int:
        return self._port

    @property
    def nogui(self) -> bool:
        return self._nogui


class LaunchingPacketTracerTimeout(LaunchingPacketTracerError):
    """This exception is used to indicate that Packet Tracer reached timeout while starting."""

    def __str__(self):
        return f'Timeout occurred while launching Packet Tracer on port {self._port} with nogui={self._nogui}'


class PortInUse(LaunchingPacketTracerError):
    """This exception is used to indicate that Packet Tracer can not start on the specified port,
    because this port is already in use by another program."""

    def __str__(self):
        return f'Port {self._port} is already in use'


class ExtractorError(Exception):
    """Base extractor error."""
    pass


class GeneralError(ExtractorError):
    """This exception is thrown when ADE failed with unknown error."""
    pass


class WrongCredentials(ExtractorError):
    """This exception is thrown when ADE contains wrong credentials."""
    pass


class ConnectionFailed(ExtractorError):
    """This exception is thrown when ADE failed to connect to Packet Tracer."""
    pass


class ArgumentsParsingError(ExtractorError):
    """This exception is thrown when ADE failed to parse args."""
    pass


class ActivityFileReadingError(ExtractorError):
    """This exception is thrown when ADE failed to read activity file."""
    pass


class ActivityNeedsPassword(ExtractorError):
    """This exception is thrown when activity file needs password, but no password was provided."""
    pass


class TopologyFilesNotSupported(ExtractorError):
    """This exception is thrown when topology file was provided to ADE instead of activity file."""
    pass


class WrongPassword(ExtractorError):
    """This exception is thrown when password that provided for activity file is wrong."""
    pass


class PacketTracerSessionError(Exception):
    """Base Packet Tracer session exception"""

    def __init__(self, port: int, nogui: bool):
        self._port = port
        self._nogui = nogui

    @property
    def port(self) -> int:
        return self._port

    @property
    def nogui(self) -> bool:
        return self._nogui


class PacketTracerSessionAlreadyRunning(PacketTracerSessionError):
    """This exception is thrown when the current session of Packet Tracer is already running and
    user tries to start a new one from the same instance of PacketTracerSession."""

    def __str__(self):
        return f'This instance of PacketTracerSession with port={self._port}, and nogui={self._nogui} is already running'


class PacketTracerSessionNotStarted(PacketTracerSessionError):
    """This exception is thrown when current PacketTracerSession is not stated yet, but user tries to stop it."""

    def __str__(self):
        return f'This instance of PacketTracerSession with port={self._port}, and nogui={self._nogui} is not started'


def _is_port_in_use(port: int) -> bool:
    """Checks if this TCP port in use.

    Args:
        port: number of port to check (from 1 to 65535)

    Returns:
        True - if port is in use, else False
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        return sock.connect_ex(('localhost', port)) == 0


def _get_free_port() -> int:
    """Returns free TCP port.

    Gets random free tcp port and returns it's number.

    Returns:
        Number of free port.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('localhost', 0))
        return sock.getsockname()[1]


def _make_params(*args, **kwargs) -> typing.Tuple[str, ...]:
    """Makes tuple with arguments to send to subprocess.run() from *args and **kwargs.

    Firstly every arg from *args stored in result tuple same order as provided.\n
    After that every kwarg from **kwargs stored in result tuple with value like: ("--param_name", "param_value")\n
    Only -- is used with arguments provided in **kwargs.\n
    If kwarg's value is None, this kwarg will be skipped.

    Args:
        *args: Arguments to store
        **kwargs: Arguments with values to store

    Examples:
        >>> _make_params(('ls', '-l'), color='always', other_argument=None)
        ('ls', '-l', '--color', 'always')

    Returns:
        A tuple with all arguments from **args and **kwargs
    """
    params = [str(arg) for arg in args]
    for name, value in kwargs.items():
        if value is not None:
            if value:
                params.append(f'--{name}')
                if type(value) != bool:
                    params.append(str(value))
    return tuple(params)


def _check_xvfb_run_installed():
    """Checks if xvfb-run is installed.

    Returns:
        True, if xvfb-run is installed, otherwise False.
    """
    completed_process = subprocess.run(('xvfb-run', '--help'),
                                       stderr=subprocess.DEVNULL,
                                       stdout=subprocess.DEVNULL)
    return completed_process.returncode == 0


def _get_process_pid_by_name(process_name: str) -> typing.Tuple[int, ...]:
    """Gets list of pids of a processes with specified process name.

    If there

    Args:
        process_name: Name of the process.

    Returns:
        Tuple with process pids.
    """
    completed_process = subprocess.run(('pidof', process_name),
                                       capture_output=True,
                                       text=True)
    pids = completed_process.stdout.strip('\n').split()
    return tuple(int(pid) for pid in pids)


def _get_process_command_by_pid(pid: int) -> str or None:
    """Gets process command by pid.

    Args:
        pid: Process pid.

    Returns:
        Process command or None if there is no process with this pid.
    """
    completed_process = subprocess.run(('ps', '-p', str(pid), '-o', 'command'),
                                       capture_output=True,
                                       text=True)
    command = completed_process.stdout.strip('\n').split('\n')[1]  # second row contains command
    return command if command else None


def _get_packet_tracer_pid(port: int) -> int or None:
    """Gets Packet Tracer pid.

    Args:
        port: IPC port.

    Returns:
        Process pid.
    """
    pids = _get_process_pid_by_name(PT_EXECUTABLE_NAME)
    for pid in pids:
        command = _get_process_command_by_pid(pid)
        if command and f'--ipc-port {port}' in command:
            return pid
    return None


def _terminate_process(pid: int, blocking=False):
    """Terminates process with specified pid.
    
    Args:
        pid: Process pid.
        blocking: If set to True, waits for process completion.
    """
    os.kill(pid, signal.SIGTERM)
    if blocking:
        os.waitpid(pid, 0)


def _launch_pt(port=39000, nogui=False, timeout: int = -1, use_virtual_display=False) -> int:
    """Launches Packet Tracer.

    Launches Packet Tracer on the specified port.\n
    If nogui is set to True, launches Packet Tracer in nogui mode (some gui objects still materialise).

    Timeout behaviour:
        * If timeout set to -1 (default), waits forever while Packet Tracer would be fully launched.
        * If timeout set to 0, immediately check if Packet Tracer is fully launched and throw an exception if not.
        * If timeout set > 0, waits for timeout seconds, check if Packet Tracer if fully launched and throw
        exception if not.

    Args:
        port: Number of the port to launch Packet Tracer on.
        nogui: If set to True, launches Packet Tracer in nogui mode.
        timeout: Timeout to launch Packet Tracer.
        use_virtual_display: If set to True, start Packet Tracer with gui in virtual display.

    Returns:
        Process pid for launched Packet Tracer.
    Raises:
        PortInUse: when provided TCP port is already in use.
        LaunchingPacketTracerError: when Packet Tracer didn't launch due to unknown error.
        LaunchingPacketTracerTimeout: when there is a timeout.
    """
    if platform.system() == 'Linux':
        ld_library_path = 'LD_LIBRARY_PATH'
        if not os.getenv(ld_library_path):
            os.environ[ld_library_path] = PT_BIN_ROOT

    # check if port is in use
    if _is_port_in_use(port):
        raise PortInUse(port, nogui)

    params = _make_params(PT_EXECUTABLE,
                          **{
                              'ipc-port': port,
                              'nogui': nogui
                          })
    if use_virtual_display:
        if _check_xvfb_run_installed():
            logger.debug('xvfb was found')
            params = _make_params('xvfb-run', '-a') + params
        else:
            logger.warning('xvfb not found, use default display')

    process = subprocess.Popen(params,
                               cwd=PT_BIN_ROOT,
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)

    if process.poll():
        raise LaunchingPacketTracerError(port, nogui)

    # wait until PT is up
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def pt_is_up():
        nonlocal sock
        return not sock.connect_ex(('localhost', port))

    if timeout == -1:
        delay = 1
        while True:
            if pt_is_up():
                break
            else:
                time.sleep(delay)

    elif timeout == 0:
        if not pt_is_up():
            _terminate_process(_get_packet_tracer_pid(port))
            raise LaunchingPacketTracerTimeout(port, nogui)

    else:
        time.sleep(timeout)
        if not pt_is_up():
            _terminate_process(_get_packet_tracer_pid(port))
            raise LaunchingPacketTracerTimeout(port, nogui)

    logger.debug(f'Packet Tracer is up on port {port}')
    return _get_packet_tracer_pid(port)


def _extract_data(port: int, filepath: str, password: str or None, read_file_timeout, net_stabilization_delay,
                  conn_attempts=5, conn_delay=100):
    """Extracts data from the activity file.

    This is a wrapper for ADE. It calls ADE and parses resulted JSON.

    Args:
        port: Number of TCP port to connect to Packet Tracer.
        filepath: Path to activity file.
        password: Password for the provided activity file.
        read_file_timeout: Timeout for ADE - time to wait when the message "Can not read this file" appears before
        decide that it is not an activity file (in seconds).
        net_stabilization_delay: Delay for net stabilization (in seconds).
        conn_attempts: Number of connection to perform.
        conn_delay: Delay between connection attempts (in milliseconds).

    Returns:
        Dict which is parsed JSON from ADE.
    Raises:
        GeneralError: when an unknown error occurred in ADE.
        WrongCredentials: when ADE has wrong credentials and can not connect to Packet Tracer.
        ConnectionFailed: when ADE failed to establish connection with Packet Tracer.
        ArgumentsParsingError: when ADE failed to parse arguments.
        ActivityFileReadingError: when ADE can not read activity file.
        WrongPassword: when wrong password was provided to specified activity.
        ActivityNeedsPassword: when no password was provided, but specified activity requires it.
        TopologyFilesNotSupported: when topology file was provided instead of activity file.
    """
    params = _make_params('java', '-Dfile.encoding=utf-8', '-jar', ADE,
                          input=filepath,
                          key=password,
                          server='localhost',
                          port=port,
                          conn_attempts=conn_attempts,
                          conn_delay=conn_delay,
                          timeout=read_file_timeout,
                          net_stabilization_delay=net_stabilization_delay)

    before = datetime.datetime.now()
    completed_process = subprocess.run(params,
                                       capture_output=True,
                                       text=True)
    after = datetime.datetime.now()
    logger.debug(f'Extracted data from {filepath}. Consumed time: {after - before}')

    error_mapping = {
        1: GeneralError,
        2: WrongCredentials,
        3: ConnectionFailed,
        4: ArgumentsParsingError,
        5: ActivityFileReadingError,
        6: None,  # an error occurred while writing data to file
        7: WrongPassword,
        8: ActivityNeedsPassword,
        9: TopologyFilesNotSupported,
    }

    if completed_process.returncode:
        error = error_mapping[completed_process.returncode]
        raise error(completed_process.stderr)

    for line in completed_process.stdout.split(os.linesep):
        first_bracket_index = line.find('{')
        last_bracket_index = line.rfind('}')
        if first_bracket_index != -1 and last_bracket_index != -1:
            try:
                return json.loads(line[first_bracket_index:last_bracket_index + 1])
            except json.JSONDecodeError:
                pass


class PacketTracerSession:
    """This class represents the Packet Tracer session.

    If no port is provided, random free TCP port will be used.

    Call start() to launch the Packet Tracer session and stop() to stop it.\n

    This class can be used as context manager:
        * When enter context - start() method is used.
        * When leave context - stop() method is used.

    Typical usage: as a parameter for extract_data() function to extract data from activity file.

    Examples:
        >>> with PacketTracerSession() as session:
        >>>     extract_data(session, 'activity.pka', 'password')
    """

    def __init__(self, port: int = 0, nogui=False, use_virtual_display=False):
        self._port = port
        self._nogui = nogui
        self._use_virtual_display = use_virtual_display
        self._pid: int = None

    def __enter__(self) -> 'PacketTracerSession':
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def __repr__(self):
        return f'{self.__class__}({self._port, self._nogui})'

    def start(self):
        # if port not provided choose random port
        self._port = self._port or _get_free_port()

        if not self._pid:
            logger.debug(f'Starting Packet Tracer session on port {self._port}')
            self._pid = _launch_pt(self._port, self._nogui, use_virtual_display=self._use_virtual_display)
        else:
            raise PacketTracerSessionAlreadyRunning(self._port, self._nogui)

    def stop(self):
        if self._pid:
            logger.debug(f'Stop Packet Tracer on port {self._port}')
            _terminate_process(self._pid)
            self._pid = None
        else:
            raise PacketTracerSessionNotStarted(self._port, self._nogui)

    @property
    def port(self) -> int:
        return self._port

    @property
    def running(self):
        return True if self._pid else False


def extract_data(session: PacketTracerSession, filepath: str, password: str or None, read_file_timeout=5,
                 net_stabilization_delay=0) -> dict:
    """Extracts data from the activity file.

    This is a wrapper for ADE. It calls ADE and parses resulted JSON.

    Args:
        session: PacketTracerSession to connect to.
        filepath: Path to activity file.
        password: Password for the provided activity file.
        read_file_timeout: Timeout for ADE - time to wait when the message "Can not read this file" appears before decide that it is not an activity file (in seconds).
        net_stabilization_delay: Delay for net stabilization (in seconds).

    Returns:
        Dict which is parsed JSON from ADE.
    Raises:
        GeneralError: when an unknown error occurred in ADE.
        WrongCredentials: when ADE has wrong credentials and can not connect to Packet Tracer.
        ConnectionFailed: when ADE failed to establish connection with Packet Tracer.
        ArgumentsParsingError: when ADE failed to parse arguments.
        ActivityFileReadingError: when ADE can not read activity file.
        WrongPassword: when wrong password was provided to specified activity.
        ActivityNeedsPassword: when no password was provided, but specified activity requires it.
        TopologyFilesNotSupported: when topology file was provided instead of activity file.
    """
    return _extract_data(session.port, filepath, password, read_file_timeout, net_stabilization_delay)


if __name__ == '__main__':
    print('This is module with functions to extract data from activity file.')
