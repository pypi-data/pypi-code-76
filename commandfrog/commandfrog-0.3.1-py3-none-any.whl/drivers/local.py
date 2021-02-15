import os
import subprocess
from typing import Optional, Union
from io import StringIO

from .driver import Driver
from .util import execute_command


class LocalHost(Driver):
    def put(self, path: str, contents: Union[str, bytes, StringIO], mode: Optional[Union[str, int]] = None):
        path = os.path.expanduser(path)

        if isinstance(contents, (str, StringIO)):
            with open(path, "w+") as text_file:
                text_file.write(contents.getvalue() if isinstance(contents, StringIO) else contents)
        else:
            with open(path, "wb+") as binary_file:
                binary_file.write(contents)

        if isinstance(mode, int):
            os.chmod(path, mode)
        elif isinstance(mode, str):
            os.chmod(path, int(mode, 8))

    def base_exec(
        self,
        cmd: str,
        echo_stdout: bool = True,
        echo_stderr: bool = True,
        assert_ok: bool = True
    ):
        return execute_command(
            cmd,
            echo_stdout=echo_stdout,
            echo_stderr=echo_stderr,
            assert_ok=assert_ok
        )


