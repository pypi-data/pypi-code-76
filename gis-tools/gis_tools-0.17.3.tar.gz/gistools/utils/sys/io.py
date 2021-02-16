# -*- coding: utf-8 -*-

""" Module summary description.

More detailed description.
"""

import base64
import ctypes
import datetime
import io
import logging
import os
import sys

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import tempfile
from contextlib import contextmanager
from tempfile import gettempdir


libc = ctypes.CDLL(None)
c_stderr = ctypes.c_void_p.in_dll(libc, 'stderr')
c_stdout = ctypes.c_void_p.in_dll(libc, 'stdout')


def decrypt(path_to_credentials, path_to_keyring, fernet_str, salt_length=16):
    """ Decrypt encrypted credentials

    :param path_to_credentials:
    :param path_to_keyring:
    :param fernet_str:
    :param salt_length:
    :return:
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=open(path_to_keyring, 'rb').read(salt_length),
        iterations=100000,
        backend=default_backend()
    )

    fernet = Fernet(base64.urlsafe_b64encode(kdf.derive(bytes(fernet_str, 'utf-8'))))

    with open(path_to_credentials, 'rb') as file:
        return fernet.decrypt(file.read(100)).decode("ascii"), fernet.decrypt(file.read()).decode("ascii")


def encrypt(path_to_credentials, path_to_keyring, user, passwd, fernet_str, salt_length=16):
    """ Encrypt credentials

    :param path_to_credentials:
    :param path_to_keyring:
    :param user:
    :param passwd:
    :param fernet_str:
    :param salt_length:
    :return:
    """
    salt = os.urandom(salt_length)
    with open(path_to_keyring, 'wb') as file:
        file.write(salt)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    fernet = Fernet(base64.urlsafe_b64encode(kdf.derive(bytes(fernet_str, 'utf-8'))))

    with open(path_to_credentials, 'wb') as file:
        file.write(fernet.encrypt(bytes(user, 'utf-8')))
        file.write(fernet.encrypt(bytes(passwd, 'utf-8')))


class LogFile:

    entry = 0

    def __init__(self, name="log_file"):
        self.path = os.path.join(gettempdir(), name + ".log")
        self.stream = io.BytesIO()

    def write(self, entry):
        with open(self.path, "a") as log_file:
            log_file.write("[%d] %s: %s\n" % (self.entry, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), entry))
        self.entry += 1

    @contextmanager
    def stdout_redirector(self):
        # The original fd stdout points to. Usually 1 on POSIX systems.
        original_stdout_fd = sys.stdout.fileno()

        def _redirect_stdout(to_fd):
            """Redirect stdout to the given file descriptor."""
            # Flush the C-level buffer stdout
            libc.fflush(c_stdout)
            # Flush and close sys.stdout - also closes the file descriptor (fd)
            sys.stdout.close()
            # Make original_stdout_fd point to the same file as to_fd
            os.dup2(to_fd, original_stdout_fd)
            # Create a new sys.stdout that points to the redirected fd
            sys.stdout = io.TextIOWrapper(os.fdopen(original_stdout_fd, 'wb'))

        # Save a copy of the original stdout fd in saved_stdout_fd
        saved_stdout_fd = os.dup(original_stdout_fd)
        tfile = tempfile.TemporaryFile(mode='w+b')
        try:
            # Create a temporary file and redirect stdout to it
            _redirect_stdout(tfile.fileno())
            # Yield to caller, then redirect stdout back to the saved fd
            yield
            _redirect_stdout(saved_stdout_fd)
            # Copy contents of temporary file to the given stream
            tfile.flush()
            tfile.seek(0, io.SEEK_SET)
            self.stream.write(tfile.read())
        finally:
            tfile.close()
            os.close(saved_stdout_fd)

        self.write(self.stream.getvalue().decode('utf-8'))

    @contextmanager
    def stderr_redirector(self):
        # The original fd stderr points to. Usually 1 on POSIX systems.
        original_stderr_fd = sys.stderr.fileno()

        def _redirect_stderr(to_fd):
            """Redirect stdout to the given file descriptor."""
            # Flush the C-level buffer stderr
            libc.fflush(c_stderr)
            # Flush and close sys.stderr - also closes the file descriptor (fd)
            sys.stderr.close()
            # Make original_stderr_fd point to the same file as to_fd
            os.dup2(to_fd, original_stderr_fd)
            # Create a new sys.stderr that points to the redirected fd
            sys.stderr = io.TextIOWrapper(os.fdopen(original_stderr_fd, 'wb'))

        # Save a copy of the original stderr fd in saved_stderr_fd
        saved_stderr_fd = os.dup(original_stderr_fd)
        tfile = tempfile.TemporaryFile(mode='w+b')
        try:
            # Create a temporary file and redirect stderr to it
            _redirect_stderr(tfile.fileno())
            # Yield to caller, then redirect stderr back to the saved fd
            yield
            _redirect_stderr(saved_stderr_fd)
            # Copy contents of temporary file to the given stream
            tfile.flush()
            tfile.seek(0, io.SEEK_SET)
            self.stream.write(tfile.read())
        finally:
            tfile.close()
            os.close(saved_stderr_fd)

        self.write(self.stream.getvalue().decode('utf-8'))


class StreamToLogger:
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, name="out", log_level=logging.INFO):
        self.path = os.path.join(tempfile.gettempdir(), name + ".log")
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''
        logging.basicConfig(level=self.log_level,
                            format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
                            filename=self.path,
                            filemode='a')

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())
