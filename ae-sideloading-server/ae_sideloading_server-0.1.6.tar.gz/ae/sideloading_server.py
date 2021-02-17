"""
sideloading server
==================

This ae namespace portion provides a simple http server for to download a file to another device in the same local
network, using any web browser.

By adding this module to your android app you can distribute e.g. the APK file of your app directly to another android
device for to install it there - without requiring an app store or an internet connection.

This portion requires the Python version 3.6 or higher. For to run multiple sideloading processes in parallel the
version 3.7 or higher is needed (providing the threaded http server :class:`~http.server.ThreadingHTTPServer` class).

The implementation is inspired by the accepted answer to `<https://stackoverflow.com/questions/18543640
/how-would-i-create-a-python-web-server-that-downloads-a-file-on-any-get-request>`_.

Useful debugging tools can be found at `<https://www.maketecheasier.com/transferring-files-using-python-http-server>`_.


sideloading server lifecycle
----------------------------

The sideloading server provided by this ae namespace portion can be started by first creating an instance of the
sideloading app and then call its :meth:`~SideloadingServerApp.start_server` method::

    from ae.sideloading_server import server_factory

    sideloading_server_app = server_factory()
    sideloading_server_app.start_server()

By calling :meth:`~SideloadingServerApp.start_server` without arguments a default file mask (:data:`DEFAULT_FILE_MASK`)
will be used, which specifies the APK file of the main app situated in the `Downloads` folder of the device.

The web address that has to be entered in the web browser of the receiving device can be determined with the
:meth:`~SideloadingServerApp.server_url` method::

    client_url = sideloading_server_app.server_url()

While the server is running the :meth:`~SideloadingServerApp.client_progress` method is providing the progress state
of any currently running sideloading task. More detailed info of the running sideloading process can be gathered
by calling the :meth:`~SideloadingServerApp.fetch_log_entries` method.

For to temporarily stop the sideloading server simple call the :meth:`~SideloadingServerApp.stop_server` method. On app
exit additionally call the method :meth:`~SideloadingServerApp.shutdown`.

.. hint::
    The ae namespace portion :mod:`ae.kivy_sideloading` is providing a package for an easy integration of this
    sideloading server into your kivy app.

    An example usage of this sideloading server and the :mod:`ae.kivy_sideloading` package is integrated into the demo
    apps `Lisz <https://gitlab.com/ae-group/kivy_lisz>`_ and `ComPartY <https://gitlab.com/ae-group/comparty>`_.

"""
import datetime
import glob
import os
import threading
from http.server import BaseHTTPRequestHandler

try:
    from http.server import ThreadingHTTPServer as HTTPServer   # type: ignore # only available from Python 3.7 onwards
except ImportError:
    from http.server import HTTPServer
from typing import Any, Callable, Dict, List, Optional, Tuple

from ae.base import DATE_TIME_ISO, os_local_ip          # type: ignore
from ae.files import copy_bytes                         # type: ignore
from ae.paths import norm_path                          # type: ignore
from ae.console import ConsoleApp                       # type: ignore


__version__ = '0.1.6'


DEFAULT_FILE_MASK = "{downloads}/{main_app_name}*.apk"     #: default glob file mask for to sideloading file
FILE_COUNT_MISMATCH = " files found matching "  #: err msg part of :meth:`SideloadingServerApp.start_server`

SERVER_BIND = ""                    #: setting BIND to '' or None for to allow connections for all local devices
SERVER_PORT = 36996                 #: http server listening port (a port number under 1024 requires root privileges)

SOCKET_BUF_LEN = 4096               #: buf length for socket sends in :meth:`~SideloadingServerApp.response_to_request`

SHUTDOWN_TIMEOUT = 3.9              #: timeout (in seconds) to shutdown/stop the console app and http sideloading server

SideloadingKwargs = Dict[str, Any]  #: command/log format of sideloading requests

clients_lock = threading.Lock()
requests_lock = threading.Lock()


def server_factory(task_id_func: Optional[Callable[[str, str, str], str]] = None) -> 'SideloadingServerApp':
    """ create server app instance.

    :param task_id_func:        callable for to return an unique id for a transfer request task.
    :return:                    sideloading server app instance.
    """
    global server_app           #: singleton server instance

    server_app = SideloadingServerApp(app_name='sideloading_server', multi_threading=True, disable_buffering=True)
    server_app.add_option('bind', "server bind address", SERVER_BIND, 'b')
    server_app.add_option('port', "server listening port", SERVER_PORT, 'p')
    server_app.add_option('file_mask', "glob file mask for the sideloading file", DEFAULT_FILE_MASK, 'm')

    if task_id_func:
        # noinspection PyTypeHints
        server_app.id_of_task = task_id_func    # type: ignore

    return server_app


def update_handler_progress(handler: Optional['SimpleHTTPRequestHandler'] = None,
                            transferred_bytes: int = -3, total_bytes: int = -3, **_kwargs):
    """ default progress update callback.

    :param handler:             server request handler - containing the attributes to be updated.
    :param transferred_bytes:   already transferred bytes or error code.
    :param total_bytes:         total sideloading bytes.
    :param _kwargs:             additional/optional kwargs (e.g. client_ip).
    """
    if handler:
        handler.progress_transferred = transferred_bytes
        handler.progress_total = total_bytes


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """ server request handler. """
    progress_total: int = -1                            #: total file size in bytes to be transferred
    progress_transferred: int = -1                      #: transferred bytes in this sideloading progress thread

    # noinspection PyPep8Naming
    def do_GET(self):
        """ handler callback for a http GET command request. """
        server_app.response_to_request(self)

    def log_request(self, code='-', size='-'):
        """ overwrite for to prevent console output if not in debug mode. """
        if server_app.debug:
            super().log_request(code=code, size=size)       # pragma: no cover


class SideloadingServerApp(ConsoleApp):
    """ server service app class """
    client_handlers: Dict[str, SimpleHTTPRequestHandler]                    #: handler for each active client connection
    file_path: str                                                          #: path to the found sideloading file
    load_requests: List[SideloadingKwargs]                                  #: sideloading requests and error/debug log
    progress_callback: Callable = lambda **_: None                          #: progress event callback
    server_instance: Optional[HTTPServer]                                   #: server class instance
    server_thread: Optional[threading.Thread]                               #: server thread (main or separate thread)

    def client_progress(self, client_ip: str) -> Tuple[int, int]:
        """ determine sideloading progress (transferred bytes) for the client with the passed ip address.

        This method can be used alternatively to the callback :attr:`~SideloadingServerApp.progress_callback`.

        :param client_ip:       client ip address.
        :return:                tuple of two int values: status and file size of the sideloading file. The
                                A positive status value signifies the number of already transferred bytes.
                                A negative value in this first int signals an error. Possibles error codes are:
                                * -1 if sideloading task did not started yet
                                * -2 if not exists or sideloading task has already finished
                                * -3 if the default
                                Please not that the file size given in the second int can be 0 if an error has occurred
                                or if the sideloading task is not yet fully created/started.
        """
        clients_lock.acquire()
        handler = self.client_handlers.get(client_ip, None)
        clients_lock.release()
        return (handler.progress_transferred, handler.progress_total) if handler else (-2, 0)

    @staticmethod
    def id_of_task(action: str, object_type: str, object_key: str) -> str:
        """ compile the id of the sideloading request task.

        :param action:          action or log level string.
        :param object_type:     task object type (currently only 'log' is implemented/supported).
        :param object_key:      task key (for log entries the timestamp of the log entry is used).
        :return:                unique key identifying the task/log-entry.
        """
        return action + '_' + object_type + ':' + object_key

    def log(self, log_level: str, message: str):
        """ print log message and optionally add it to the requests (for to be read by controller app).

        :param log_level:       'print' always prints, 'debug' prints if self.debug, 'verbose' prints if self.verbose.
        :param message:         message to print.
        """
        out_method = getattr(self, log_level + '_out', None)
        if callable(out_method):
            out_method(("" if self.active_log_stream else f"{threading.current_thread().name: <15}") + f"{message}")

        if getattr(self, log_level, True):
            log_time = datetime.datetime.now()

            requests_lock.acquire()
            self.load_requests.append(dict(
                method_name=log_level + '_' + 'log', message=message,
                log_time=log_time, rt_id=self.id_of_task(log_level, 'log', log_time.strftime(DATE_TIME_ISO))))
            requests_lock.release()

    def fetch_log_entries(self) -> Dict[str, SideloadingKwargs]:
        """ collect last log entries, return them and remove them from this app instance.

        :return:                Dict[request_tasks_id, sideloading_request_kwargs] with fetched requests log entries.
        """
        requests_lock.acquire()
        log_entries = dict()
        requests = self.load_requests
        for entry in requests:
            log_entries[entry['rt_id']] = entry
        requests[:] = list()
        requests_lock.release()

        return log_entries

    def response_to_request(self, handler: SimpleHTTPRequestHandler):
        """ process request to this server and return response string.

        .. note:: this method may run in a separate thread (created by the server for to process this request).

        :param handler:         stream request handler instance.
        """
        pre = "SideloadingServerApp.response_to_request()"
        self.log('verbose', f"{pre} from client={handler.client_address}")
        client_ip = handler.client_address[0]
        clients_lock.acquire()
        self.client_handlers[client_ip] = handler   # removed by controlling process/app on finished sideloading
        clients_lock.release()

        errors: List[str] = list()
        try:
            handler.send_response(200)
            handler.send_header("Content-Type", 'application/octet-stream')
            handler.send_header("Content-Disposition", f'attachment; filename="{os.path.basename(self.file_path)}"')
            with open(self.file_path, 'rb') as file_handle:
                file_size = os.fstat(file_handle.fileno()).st_size
                handler.progress_total = file_size
                handler.send_header("Content-Length", str(file_size))
                handler.end_headers()

                progress_kwargs = dict(client_ip=client_ip, handler=handler)
                copy_bytes(file_handle, handler.wfile, total_bytes=file_size, buf_size=SOCKET_BUF_LEN, errors=errors,
                           progress_func=self.progress_callback, **progress_kwargs)
                if errors:
                    self.log('print', f"{pre} copy_bytes errors: {errors}")
                else:
                    handler.progress_transferred = file_size

        except (KeyError, IOError, OSError, SyntaxError, ValueError, Exception) as ex:
            self.log('print', f"{pre} exception {ex} on send of {self.file_path}")

        else:
            if not errors:
                self.log('debug', f"{pre} side-loaded {file_size} bytes of {self.file_path} to {client_ip}")

    def server_url(self) -> str:
        """ determine a url string for to put into the address field of any browser for to start sideloading.

        :return:                server url string.
        """
        url = "http://" + os_local_ip()
        port = self.get_opt('port')
        if port != 80:
            url += ":" + str(port)
        return url

    def shutdown(self, exit_code: Optional[int] = 0, timeout: Optional[float] = None):
        """ overwritten for to stop any running sideloading server instance/threads on shutdown of this app instance.

        :param exit_code:   set application OS exit code - see :meth:`~ae.core.AppBase.shutdown`.
        :param timeout:     timeout float value in seconds - see :meth:`~ae.core.AppBase.shutdown`.
        """
        self.stop_server()
        super().shutdown(exit_code=exit_code, timeout=timeout)

    def start_server(self, file_mask: str = "", threaded: bool = False, progress: Callable = update_handler_progress
                     ) -> str:
        """ start http file sideloading server to run until :meth:`~.stop_server` get called.

        :param file_mask:       optional glob.glob file mask to specify the sideloading file. If not passed then
                                the :data:`DEFAULT_FILE_MASK` will be used which specifies a APK file of the
                                main app situated in the `Downloads` folder of the device.
                                The sideloading server will only be started if the file mask matches exactly one file.
                                The file path of the matched file can be accessed via the
                                :attr:`~SideloadingServerApp.file_path` attribute.
        :param threaded:        optionally pass True to use separate thread to run the server instance.
        :param progress:        optional callback executed for each transferred/side-loaded chunk. If not specified
                                then the default callback method :func:`update_handler_progress`
                                will be called for to update the progress attributes of the request handler, which can
                                be polled via the :meth:`~SideloadingServerApp.client_progress` method.
        :return:                empty string/"" if server instance/thread got started else the error message string.
        """
        pre = "SideloadingServerApp.start_server()"
        if not file_mask:
            file_mask = self.get_opt('file_mask', DEFAULT_FILE_MASK)
        self.progress_callback = progress                                                       # type: ignore

        self.server_instance = self.server_thread = None
        self.client_handlers = dict()
        self.load_requests = list()

        if requests_lock.locked():  # pragma: no cover
            requests_lock.release()             # release before self.log() call (new acquiring)
            self.log('print', f"{pre}: released requests lock")
        if clients_lock.locked():   # pragma: no cover
            self.log('print', f"{pre}: releasing clients lock")
            clients_lock.release()

        self.log('debug', f"{pre}: {'threaded' if threaded else ''} with file mask='{file_mask}' and cb={progress}")

        err_msg = ""
        try:
            files = glob.glob(norm_path(file_mask))
            file_count = len(files)
            if file_count != 1:
                return f"{pre}: {str(file_count) if file_count else 'no'}{FILE_COUNT_MISMATCH}{file_mask}"
            self.file_path = files[0]

            server_address = (self.get_opt('bind'), self.get_opt('port'))
            HTTPServer.allow_reuse_address = True
            SimpleHTTPRequestHandler.protocol_version = "HTTP/1.0"
            self.server_instance = HTTPServer(server_address, SimpleHTTPRequestHandler)
            self.server_instance.timeout = SHUTDOWN_TIMEOUT

            self.log('verbose', f"{pre}: {self.file_path} (ip,port)={server_address}"
                                f"/{self.server_instance.server_address}"
                                f"/{self.server_instance.socket.getsockname()}")
            tct = threading.current_thread()
            if threaded:
                # Start a thread with the server -- that thread will then start one more thread for each request
                self.server_thread = threading.Thread(name="SideloadingTrd", target=self.server_instance.serve_forever)
                self.server_thread.start()
                self.log('verbose', f"{pre}: started server from thread={tct.name} in thread={self.server_thread.name}")
            else:
                self.log('verbose', f"{pre}: starting server loop; blocking this main thread={tct.name}")
                self.server_thread = tct
                self.server_instance.serve_forever()

        except (IOError, OSError, Exception) as ex:
            err_msg = f"{pre}: exception {ex}"
            self.log('print', err_msg)
            self.server_instance = self.server_thread = None

        return err_msg

    def stop_server(self):
        """ stop/pause sideloading server - callable also if not running to reset/prepare this app instance. """
        pre = "SideloadingServerApp.stop_server()"
        if requests_lock.locked():  # pragma: no cover
            requests_lock.release()             # release before self.log() call (new acquiring)
            self.log('print', f"{pre}: released requests lock")
        if clients_lock.locked():   # pragma: no cover
            self.log('print', f"{pre}: releasing clients lock")
            clients_lock.release()
        self.log('verbose', f"{pre}")

        if getattr(self, 'server_instance', False) and getattr(self, 'server_thread', False):
            if self.server_thread == threading.current_thread():                # pragma: no cover
                thread = threading.Thread(name="StopSideloadingServerThread", target=self.server_instance.shutdown)
                thread.start()
                thread.join(timeout=SHUTDOWN_TIMEOUT)
                if thread.is_alive():
                    self.log('print', f"{pre}: server shutdown thread join timed out")
            else:
                self.server_instance.shutdown()
                self.server_thread.join(timeout=SHUTDOWN_TIMEOUT)
                if self.server_thread.is_alive():
                    self.log('print', f"{pre}: server thread join timed out")   # pragma: no cover
        self.server_instance = self.server_thread = None


if __name__ == '__main__':              # pragma: no cover
    server_app = server_factory()
    server_app.run_app()
    server_app.start_server()
