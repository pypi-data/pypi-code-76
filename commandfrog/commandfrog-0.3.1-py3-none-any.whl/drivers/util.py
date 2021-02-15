from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
import subprocess
import sys
from typing import BinaryIO

from loguru import logger

from .driver import Result
from .exceptions import CommandFailed


def execute_command(
    cmd: str,
    echo_stdout: bool = True,
    echo_stderr: bool = True,
    assert_ok: bool = True
):
    stdout_bytes = BytesIO()
    stderr_bytes = BytesIO()
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True) as proc:
        with ThreadPoolExecutor(2) as pool:
            r1 = pool.submit(log_popen_pipe, proc, proc.stdout, stdout_bytes, echo=echo_stdout)
            r2 = pool.submit(log_popen_pipe, proc, proc.stderr, stderr_bytes, echo=echo_stderr)
            r1.result()
            r2.result()
        if assert_ok and proc.returncode != 0:
            raise CommandFailed(cmd, stdout_bytes.getvalue(), stderr_bytes.getvalue())
        return Result(proc.returncode, stdout_bytes.getvalue(), stderr_bytes.getvalue())


def log_popen_pipe(proc: subprocess.Popen, in_fp: BinaryIO, out_fp: BinaryIO, echo: bool):
    while proc.poll() is None:
        line = in_fp.readline()
        if echo:
            log_output_line(line.decode(), end='')
        out_fp.write(line)

    # Write the rest from the buffer
    rest = in_fp.read()
    if rest:
        if echo:
            log_output_line(rest.decode(), end='')
        out_fp.write(rest)


def log_output_line(line: str, end: str = '\n'):
    print(line, file=sys.stderr, end=end)
