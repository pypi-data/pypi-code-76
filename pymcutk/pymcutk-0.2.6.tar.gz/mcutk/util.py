from __future__ import print_function
import os
import sys
import signal
import stat
import shutil
import shlex
import logging
import subprocess
import threading
from threading import Timer
from distutils.version import LooseVersion
from mcutk.exceptions import ProcessTimeout

PY = sys.version_info[0]

"""
This module provide some useful functions.
"""

def to_hex(val):
    """ Safe to convert to hex"""

    if type(val) == str:
        return val
    return format(val, 'x')


def _readerthread(fh, buffer, need_print):
    while True:
        stdoutdata = fh.readline()
        if stdoutdata:
            if need_print:
                sys.stdout.write(stdoutdata)
                sys.stdout.flush()
            buffer.append(stdoutdata)
        else:
            break

def run_command(cmd, cwd=None, shell=True, stdout=False, timeout=None, need_raise=False):
    """Run a command with a timeout timer and capture it's console output.

    This method wrapped subprocess.Popen, when you need to capture console output, just make
    sure **stdout** is True.

    Arguments:
        cmd -- {str or list} command string or list, like subprocess
        cwd -- {str} process work directory.
        shell -- {boolean} Use shell or not.
        stdout -- {boolean} Capture stdout and print it in real time. Choices: capture, caputure_print.
                    stdout=True means it will do caputure_print, set to False to disable capture stdout.
        timeout -- {int} timeout in seconds, default: None
        need_raise -- {boolean} a switch to disable raising ProcessTimeout exception,
                    just logging it as an error message, default: False.

    Returns:
        Tuple -- (returncode, output)
    """
    output = ""
    returncode, timer, error_message = None, None, None
    timer_result = {"is_timeout": False}

    if shell:
        # python documentation:
        # On Windows, The shell argument (which defaults to False) specifies
        # whether to use the shell as the program to execute.
        # If shell is True, it is recommended to pass args as a string rather
        # than as a sequence.
        if isinstance(cmd, list):
            cmd = " ".join(cmd)
    else:
        # Windows platform, convert cmd to list to will lead out the slash issue.
        if os.name == 'nt':
            if not isinstance(cmd, list):
                cmd = shlex.split(cmd)

    kwargs = {
        "stdout": subprocess.PIPE if stdout else None,
        "stderr": subprocess.STDOUT,
        "cwd": cwd,
        "shell": shell
    }

    if PY > 2:
        kwargs['encoding'] = 'utf8'

    try:
        process = subprocess.Popen(cmd, **kwargs)

        # start timer
        if timeout:
            timer = Timer(timeout, _timeout_trigger, args=(process, timer_result, ))
            timer.start()

        if stdout:
            need_print = False
            if stdout == "capture_print" or stdout == True:
                need_print = True
            output = []
            stdout_thread = threading.Thread(
                target=_readerthread,
                args=(process.stdout, output, need_print))
            stdout_thread.setDaemon(True)
            stdout_thread.start()

            process.wait()
            stdout_thread.join()
            output = ''.join(output)
        else:
            output, error = process.communicate()

        returncode = process.returncode

        if returncode != 0:
            error_message = 'Error: {0}\n  exit code:  {1}\n'.format(cmd, process.pid)
            if output:
                error_message += ' console output: %s'%(output)
            logging.debug(error_message)

    except OSError as emsg:
        logging.exception(emsg)

    finally:
        if timer:
            timer.cancel()

        if timer_result['is_timeout']:
            msg = "process(pid %s) timeout(%ss)" % (process.pid, timeout)
            if need_raise:
                raise ProcessTimeout(msg)
            else:
                logging.error(msg)

    return returncode, output



def _timeout_trigger(pro, result):
    """Timeout will kill the group processes.

    [Timeout will kill the group processes]

    Arguments:
        pro {Popen object} -- process
    """

    if os.name == "nt":
        subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=pro.pid))
    else:
        pro.terminate()

    if isinstance(result, dict):
        result['is_timeout'] = True


def rmtree(path):
    """Remove directory tree. If failed , it will check the access and force
    to close unclosed handler, then try remove agagin.
    """
    try:
        shutil.rmtree(path)
    except Exception:
        # Is the error an access error ?
        if not os.access(path, os.W_OK):
            os.chmod(path, stat.S_IWUSR)

        # Readonly on windows
        if os.name == "nt":
            subprocess.check_call(('attrib -R ' + path + '\\* /S').split())

        shutil.rmtree(path)



def onerrorHandler(func, path, exc_info):
    """Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.

    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    if not os.access(path, os.W_OK):
        # Is the error an access error ?
        os.chmod(path, stat.S_IWUSR)
        func(path)


def copydir(root_src_dir, root_dst_dir):
    """Copy directory to dst dir."""
    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = os.path.normpath(src_dir.replace(root_src_dir, root_dst_dir, 1))
        print("copying %s"%dst_dir)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.normpath(os.path.join(src_dir, file_))
            dst_file = os.path.normpath(os.path.join(dst_dir, file_))
            if os.path.exists(dst_file):
                os.chmod(dst_file, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO) # 0777
                os.remove(dst_file)
            shutil.copy(src_file, dst_file)


def get_max_version(version_pool):
    versions = [(ver[0], LooseVersion(str(ver[1]))) for ver in version_pool]
    versions.sort(key=lambda x: x[1])
    return versions[-1]
