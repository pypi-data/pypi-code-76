import socket
import sys
import logging

import paramiko


class SSHClient(object):
    def __init__(self, exit_on_fail=True, verbose=True):
        self.logger = logging.getLogger(type(self).__name__)
        self._exit_on_fail = exit_on_fail
        self._ssh = paramiko.SSHClient()
        self._ssh.load_system_host_keys()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._connected = False
        self.verbose = verbose

    def connect(self, server, username, password) -> bool:
        try:
            self._ssh.connect(
                hostname=server, username=username, password=password
            )
            self._connected = True
            return True
        except socket.gaierror:
            self.logger.error(
                "Failed to connect to server: {}@{} (socket.gaierror)".format(
                    username, server
                )
            )
            if self._exit_on_fail:
                self.logger.error(
                    "Run `solitude config test` to test the current configuration."
                )
                sys.exit()
        except Exception as e:
            if self._exit_on_fail:
                raise e
            else:
                self.logger.error("Failed with: {}".format(e))
        return False

    def is_connected(self) -> bool:
        return self._connected

    def exec_command(self, cmd_to_execute):
        if not self.is_connected():
            if not self.connect():
                return None
        if self.verbose:
            self.logger.info("CMD: {}".format(cmd_to_execute))
        try:
            ssh_stdin, ssh_stdout, ssh_stderr = self._ssh.exec_command(
                cmd_to_execute
            )
            result = (
                "".join(ssh_stdout.readlines()),
                "".join(ssh_stderr.readlines()),
            )
            if self.verbose:
                self.logger.info("RESULT: {}".format(result[0]))
            return result
        except Exception as e:
            self.logger.error("Failed with: {}".format(e))
            if self._exit_on_fail:
                sys.exit()
        return None
