import inspect
import sys
from .utils import Client
import threading
from threading import Thread
import asyncio
import atexit
import time
import uuid
import os
import ctypes
import logging
import aiohttp

debugger = threading.local()
debugger.instance = None

_logger = logging.getLogger(__name__)


class StopDebugger(Exception):
    pass


def safe_serialize_dict(obj):
    res = {}
    for key, value in obj.items():
        if isinstance(value, (str, int, float, )):
            res[key] = value
        else:
            try:
                res[key] = repr(value)
            except Exception:
                res[key] = "Couldn't convert to string"
    return res


def safe_serialize_tuple(obj):
    if isinstance(obj, tuple):
        return [
            repr(val)
            for val in obj
        ]
    else:
        return repr(obj)


class DbClient(Client):
    def __init__(self, websocket, debugger):
        super(DbClient, self).__init__(websocket)
        self.debugger = debugger
        debugger.client_obj = self
        self.break_files = []

    async def on_read(self, data):
        if (
            data.get("action") == "configure" and
            data.get('type') == 'break'
        ):
            self.break_files = data.get('files')
            return

        if (
            data.get("action") == "interrupt"
        ):
            self.debugger.mode = 'step'

        if (
            data.get("action") == "stop"
        ):
            await self.stop()

        await super(DbClient, self).on_read(data)

    async def on_write(self, data):
        pass

    # async def event_loop(self):
    #     if self.debugger.stopped:
    #         self.on_exit()
    #         return
    #     await super(Client, self).event_loop()


class FakeDebugger(object):
    def __init__(self):
        self.stopped = True

    def stop(self):
        pass


def client_thread(parent_debugger):
    try:
        if debugger.instance:
            debugger.instance.stopped = True
    except Exception:
        debugger.instance = FakeDebugger()

    def get_tags():
        env = os.environ.copy()
        tags = []
        for key, value in env.items():
            if key.startswith('AWDB_TAGS_'):
                tags += [
                    val.strip()
                    for val in value.split(',')
                ]

        tags.append("thread:{}".format(threading.current_thread().getName()))

        return tags

    async def connect():
        try:
            HOSTNAME = os.environ.get('AWDB_URL', 'wss://awdb.docker/ws')
            VERIFY_SSL = os.environ.get('AWDB_VERIFY_SSL', 'TRUE')
            verify_ssl = VERIFY_SSL == "TRUE"
            connector = aiohttp.TCPConnector(verify_ssl=verify_ssl)
            session = aiohttp.ClientSession(connector=connector)
            websocket = await session.ws_connect(HOSTNAME)

            client = DbClient(websocket, parent_debugger)
            client.loop = asyncio.get_event_loop()
            client.uuid = uuid.uuid1()

            init_session = {
                "event": "new_session",
                "uuid": client.uuid.hex,
                "tags": get_tags()
            }

            await websocket.send_json(init_session)

            while True:
                if parent_debugger.stopped:
                    await client.stop()
                    return

                await client.event_loop()

            _logger.debug("Ended client")
            await session.close()
        except Exception:
            _logger.info("Exception occured exiting task cleanly")

    loop = asyncio.new_event_loop()
    task = asyncio.ensure_future(connect(), loop=loop)
    loop.run_until_complete(task)
    parent_debugger.stopped = True


class Debugger(object):
    def __init__(self):
        self.client = Thread(target=client_thread, args=(self,), daemon=True)
        self.client.start()
        self.client_obj = None
        self.stopped = False

        self.thread_name = threading.current_thread().getName()
        self.breakpoints = []
        self.mode = 'step'
        self.break_on_return = False
        self.return_frame = None

        while not self.client_obj and not self.stopped:
            _logger.debug(
                "[%s] Waiting for the client from the async thread ",
                self.thread_name
            )
            time.sleep(1)

    def test_breakpoints(self, frame, event):
        filename = frame.f_code.co_filename
        lineno = frame.f_lineno

        for b_event, b_lineno, b_filename in self.breakpoints:
            event_match = b_event == event or b_event == 'any'
            filename_match = b_filename == filename or b_filename == 'any'

            if b_lineno == 'any':
                lineno_match = True
            else:
                if isinstance(b_lineno, (tuple, list)):
                    lineno_match = b_lineno[0] <= lineno <= b_lineno[1]
                else:
                    lineno_match = b_lineno == lineno

            _logger.debug(
                "{} {} {}".format(
                    (event, b_event, event == b_event),
                    (lineno, b_lineno, lineno == b_lineno),
                    (filename, b_filename, filename == b_filename),
                )
            )

            if all([event_match, filename_match, lineno_match]):
                return True

    def should_break(self, frame, event, arg):
        if (
            self.break_on_return and
            event == 'return' and
            frame == self.return_frame
        ):
            self.break_on_return = False
            return True

        if self.test_breakpoints(frame, event):
            return True

        if self.mode == 'step':
            return True

        return False

    def inspect_frame(self, frame, event, arg):
        source_code, source_line = inspect.getsourcelines(frame.f_code)
        source = "".join(source_code)
        frame_locals = safe_serialize_dict(frame.f_locals)
        frame_globals = safe_serialize_dict(frame.f_globals)

        data = {
            "type": "frame",
            "session": self.client_obj.uuid.hex,
            "event": event,
            "arg": safe_serialize_tuple(arg),
            "source": source,
            "source_lineno": source_line,
            "lineno": frame.f_lineno,
            "filename": frame.f_code.co_filename,
            "locals": frame_locals,
            "globals": frame_globals
        }

        return data

    def __call__(self, frame, event, arg):
        if self.stopped or not self.client_obj:
            return

        if not self.should_break(frame, event, arg):
            return self

        thread_name = threading.current_thread().getName()
        _logger.debug(
            "Start Trace (%s) %s %s",
            thread_name,
            event,
            arg
        )

        data = self.inspect_frame(frame, event, arg)

        frame_stack = []
        current_frame = frame

        self.send_queue(data)

        while True:
            obj = self.receive_queue()

            if isinstance(obj, StopDebugger):
                return self

            if obj['action'] in ['step', 's']:
                self.mode = 'step'
                return self
            if obj['action'] in ['return', 'r']:
                self.break_on_return = True
                self.return_frame = frame
                self.mode = 'continue'
                return self
            elif obj['action'] == 'stop':
                _logger.debug("[%s] Removing trace to continue", thread_name)
                self.mode = 'step'
                sys.settrace(None)
                return
            elif obj['action'] in ['continue', 'c']:
                _logger.debug("[%s] Removing trace to continue", thread_name)
                self.mode = 'continue'
                return self
            elif obj.get('action') == 'set_locals':
                current_frame.f_locals.update({
                    obj.get('key'): obj.get('value')
                })
                ctypes.pythonapi.PyFrame_LocalsToFast(
                    ctypes.py_object(current_frame), ctypes.c_int(0)
                )
            elif obj.get('action') == 'execute':
                try:
                    code = compile(obj.get('code'), '<eval>', 'eval')
                    ret_val = eval(
                        code, current_frame.f_globals, current_frame.f_locals,
                    )
                except Exception:
                    local_values = current_frame.f_locals.copy()
                    try:
                        code = compile(obj.get('code'), '<exec>', 'exec')
                        ret_val = eval(
                            code, current_frame.f_globals, local_values
                        )
                        current_frame.f_locals.update(local_values)
                        ctypes.pythonapi.PyFrame_LocalsToFast(
                            ctypes.py_object(current_frame), ctypes.c_int(0)
                        )
                    except Exception:
                        _logger.error("Got error", exc_info=True)
                        ret_val = None

                self.send_queue({
                    "type": "retval",
                    "value": repr(ret_val)
                })
            elif obj.get('action') == 'add_breakpoint':
                _logger.debug("Adding breakpoint")
                self.breakpoints.append(obj.get('breakpoint'))
            elif obj.get('action') == 'remove_breakpoint':
                self.breakpoints.remove(obj.get('breakpoint'))
            elif obj.get('action') == 'breakpoints':
                self.send_queue({
                    "type": "breakpoints",
                    "breakpoints": list(self.breakpoints)
                })
            elif obj.get('action') == 'inspect':
                data = self.inspect_frame(current_frame, event, arg)
                self.send_queue(data)
            elif obj.get('action') == 'up':
                if (current_frame.f_back):
                    frame_stack.append(current_frame)
                    current_frame = current_frame.f_back
                data = self.inspect_frame(current_frame, event, arg)
                self.send_queue(data)
            elif obj.get('action') == 'down':
                if len(frame_stack) > 0:
                    current_frame = frame_stack.pop()
                data = self.inspect_frame(current_frame, event, arg)
                self.send_queue(data)
            elif obj.get('action') == 'w':
                action = self.get_call_stack(current_frame)
                self.send_queue(action)
            else:
                _logger.info(
                    "Unknown command waiting for next command"
                )

            self.send_queue({'action': 'none'})

        return self

    def get_call_stack(self, frame):
        frames = inspect.getouterframes(frame)

        frames.reverse()

        return {
            "type": "frames",
            "frames": [
                {
                    "filename": info.filename,
                    "lineno": info.lineno,
                    "function": info.function
                }
                for info in frames
            ]
        }

    def send_queue(self, data):
        queue = self.client_obj.send_queue

        async def put_queue(data):
            _logger.debug("Put data into queue")
            return await queue.put(data)

        loop = self.client_obj.loop
        asyncio.run_coroutine_threadsafe(put_queue(data), loop).result()

    def receive_queue(self):
        async def get_queue():
            sleep_task = asyncio.ensure_future(asyncio.sleep(1))
            get_task = asyncio.ensure_future(self.client_obj.recv_queue.get())

            while True:
                done, pending = await asyncio.wait(
                    [sleep_task, get_task],
                    return_when=asyncio.FIRST_COMPLETED
                )
                if get_task in done:
                    return await get_task
                else:
                    await sleep_task

                if self.client_obj.stopped:
                    return StopDebugger()

                sleep_task = asyncio.ensure_future(asyncio.sleep(1))

            return await self.client_obj.recv_queue.get()

        loop = self.client_obj.loop
        return asyncio.run_coroutine_threadsafe(get_queue(), loop).result()

    def stop(self):
        self.stopped = True

        if sys.gettrace() == self:
            sys.settrace(None)

        if self.client_obj:
            self.client_obj.stopped = True

        self.client.join()


def set_trace():
    _logger.debug("[%s] Set trace", threading.current_thread().getName())
    thread_name = threading.current_thread().getName()

    try:
        instance = debugger.instance
        if not instance or instance.stopped:
            debugger.instance = Debugger()
            instance = debugger.instance
    except Exception:
        debugger.instance = Debugger()
        instance = debugger.instance

    def destroy(instance):
        def wrap():
            _logger.debug("[%s] Destroying debugger instance", thread_name)
            instance.stop()
        return wrap

    atexit.register(destroy(instance))

    frame = sys._getframe().f_back
    while frame:
        frame.f_trace = instance
        frame = frame.f_back

    if not instance.stopped:
        instance.mode = 'step'
        _logger.debug("[%s] Set trace to %s", thread_name, instance)
        sys.settrace(instance)
    else:
        _logger.debug("[%s] Remove trace", thread_name)
        sys.settrace(None)
