"""Handles communication on the backend side between frontend and backend"""
from __future__ import print_function, unicode_literals

import json
import os
import sys
import traceback


class MissingCommand(TypeError):
    """Missing command"""


class BackendProxy:
    def __init__(self, backend_module, backend_obj):
        self.backend_module = backend_module
        self.backend_object = backend_obj
        backend = __import__(self.backend_module, fromlist=[None])  # type: ignore[list-item]
        if self.backend_object:
            backend = getattr(backend, self.backend_object)
        self.backend = backend

    def __call__(self, name, *args, **kwargs):
        on_object = self if name.startswith("_") else self.backend
        if not hasattr(on_object, name):
            raise MissingCommand("{!r} has no attribute {!r}".format(on_object, name))
        return getattr(on_object, name)(*args, **kwargs)

    def __str__(self):
        return "{}(backend={})".format(self.__class__.__name__, self.backend)

    def _exit(self):  # noqa
        return 0


def flush():
    sys.stderr.flush()
    sys.stdout.flush()


def run(argv):
    reuse_process = argv[0].lower() == "true"

    try:
        backend_proxy = BackendProxy(argv[1], None if len(argv) == 2 else argv[2])
    except BaseException:
        print("failed to start backend", file=sys.stderr)
        raise
    else:
        print("started backend {}".format(backend_proxy), file=sys.stdout)
    finally:
        flush()  # pragma: no branch
    while True:
        content = read_line()
        if not content:
            continue
        flush()  # flush any output generated before
        try:
            if sys.version_info[0] == 2:  # pragma: no branch # python 2 does not support loading from bytearray
                content = content.decode()  # pragma: no cover
            parsed_message = json.loads(content)
            result_file = parsed_message["result"]
        except Exception:  # noqa
            # ignore messages that are not valid JSON and contain a valid result path
            print("Backend: incorrect request to backend: {}".format(content), file=sys.stderr)
            flush()
        else:
            result = {}
            try:
                cmd = parsed_message["cmd"]
                print("Backend: run command {} with args {}".format(cmd, parsed_message["kwargs"]))
                outcome = backend_proxy(parsed_message["cmd"], **parsed_message["kwargs"])
                result["return"] = outcome
                if cmd == "_exit":
                    break
            except BaseException as exception:
                result["code"] = exception.code if isinstance(exception, SystemExit) else 1
                result["exc_type"] = exception.__class__.__name__
                result["exc_msg"] = str(exception)
                if not isinstance(exception, MissingCommand):  # for missing command do not print stack
                    traceback.print_exc()
                if not isinstance(exception, Exception):  # allow SystemExit/KeyboardInterrupt to go through
                    raise
            finally:
                try:
                    with open(result_file, "wt") as file_handler:
                        json.dump(result, file_handler)
                except Exception:  # noqa
                    traceback.print_exc()
                finally:
                    # used as done marker by frontend
                    print("Backend: Wrote response {} to {}".format(result, result_file))
                    flush()  # pragma: no branch
        if reuse_process is False:  # pragma: no branch # no test for reuse process in root test env
            break
    return 0


def read_line():
    # for some reason input() seems to break (hangs forever) so instead we read byte by byte the unbuffered stream
    content = bytearray()
    while True:
        try:
            char = os.read(0, 1)
        except EOFError:  # pragma: no cover # when the stdout is closed without exit
            break  # pragma: no cover
        if char == b"\n":  # pragma: no cover
            break
        if char != b"\r":  # pragma: win32 cover
            content += char
    return content


if __name__ == "__main__":
    sys.exit(run(sys.argv[1:]))
