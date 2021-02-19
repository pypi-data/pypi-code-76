from .remote_exec import RemoteExec, RemoteError
import os, logging

logger = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])


class RemoteFunctions(RemoteExec):

    def __init__(self, remote_exec):
        self._remote = remote_exec

    def exec(self, code, output=None):
        return self._remote.exec(code, output)

    def softreset(self):
        self._remote.softreset()

    def eval_exec(self, code: str, output=None) -> None:
        self.exec(_eval_exec.format(repr(code)), output)

    def uid(self):
        """uid of remote, no permanent code upload"""
        return self.exec(_uid).decode()

    def implementation(self):
        return self.exec("import sys; print(sys.implementation.name, end='')").decode()

    def DEPRECEATE_eval_func(self, func, *args, output=None, **kwargs) -> str:
        """Call func(*args, **kwargs) on (Micro)Python board."""
        try:
            logger.debug(f"eval_func: {func}({args})")
            args_arr = [repr(i) for i in args]
            kwargs_arr = ["{}={}".format(k, repr(v)) for k, v in kwargs.items()]
            func_str = inspect.getsource(func)
            func_str += 'import os\n'
            func_str += 'os.chdir("/")\n'
            func_str += 'result = ' + func.__name__ + '('
            func_str += ', '.join(args_arr + kwargs_arr)
            func_str += ')\n'
            func_str += 'if result: print(result)\n'
            logger.debug(f"eval_func: {func_str}")
            start_time = time.monotonic()
            result = self.exec(func_str, output)
            if result:
                try:
                    result = result.decode().strip()
                except UnicodeDecodeError:
                    logger.error(f"UnicodeDecodeError {result}")
                    result = str(result)
            logger.debug(f"eval_func: {func.__name__}({repr(args)[1:-1]}) --> {result},   in {time.monotonic()-start_time:.3} s")
            return result
        except SyntaxError as se:
            logger.error(f"Syntax {se}")

    def _remote_exec(self, output, code):
        try:
            return self._remote.exec(f"exec({repr(code), __iot49__}", output)
        except NameError as e:
            # upload function code and try again
            print("NameError:", dir(e))
            self._remote.exec(f"import os\n__iot49__ = {'{}'}\n{_remote_functions}")
            return self._remote.exec(f"exec({repr(code), __iot49__}", output)

    def cat(self, output, path):
        self._remote_exec(output, f"cat({repr(path)})")


###############################################################################
# code snippets (run on remote)

_eval_exec = """
_iot49_ = {}
try:
    eval(compile(_iot49_, '<string>', 'single'))
except SyntaxError:
    exec(_iot49_)
finally:
    del _iot49_
"""

_uid = """
try:
    import machine
    print(":".join("{:02x}".format(x) for x in machine.unique_id()), end="")
except:
    import microcontroller
    print(":".join("{:02x}".format(x) for x in microcontroller.cpu.uid), end="")
"""
