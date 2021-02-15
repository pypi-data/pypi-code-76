import getpass
import os
import select
from io import StringIO
import shlex
from typing import Dict, Optional, Union

from loguru import logger
import paramiko

from commandfrog.config import Config
from .driver import Driver, Result
from .util import log_output_line
from .exceptions import CommandFailed

class SSHHost(Driver):
    has_sudo = True

    def __init__(
        self,
        config: Config,
        hostname: str,
        username: str,
        key: str = None,
    ):
        super().__init__(config=config)
        ssh_config = paramiko.SSHConfig()
        user_config_file = os.path.expanduser("~/.ssh/config")
        if os.path.exists(user_config_file):
            with open(user_config_file) as f:
                ssh_config.parse(f)

        # Thanks https://gist.github.com/acdha/6064215
        user_config = ssh_config.lookup(hostname)
        if 'hostname' in user_config:
            hostname = user_config['hostname']
        if 'user' in user_config:
            username = user_config['user']
        if 'identityfile' in user_config:
            key = user_config['identityfile'][0]

        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())
        self.client.connect(
            hostname=hostname,
            username=username,
            pkey=paramiko.RSAKey.from_private_key_file(key or os.path.expanduser("~/.ssh/id_rsa")),
        )
        self.env: Dict[str, str] = {}

    def put(self, path: str, contents: Union[str, StringIO, bytes], mode: Optional[Union[str, int]] = None):
        ftp_client = self.client.open_sftp()

        #TODO-master
        c = StringIO(contents) if isinstance(contents, str) else contents
        ftp_client.putfo(c, path)
        if mode is not None:
            if isinstance(mode, int):
                mode_arg = oct(mode)[2:]
            else:
                mode_arg = mode
            stdin, stdout, stderr = self.client.exec_command(f"chmod {mode_arg} {path}")

    def base_exec(
        self,
        cmd: str,
        assert_ok: bool = True,
        echo_stdout: bool = True,
        echo_stderr: bool = True
    ):
        result = stream_exec(self.client, cmd)
        if assert_ok and result.return_code != 0:
            raise CommandFailed(cmd, result.stdout, result.stderr)
        return result


def stream_exec(ssh: paramiko.SSHClient, cmd: str):
    # https://stackoverflow.com/a/32758464/223486
    # one channel per command
    stdin, stdout, stderr = ssh.exec_command(cmd)
    # get the shared channel for stdout/stderr/stdin
    channel = stdout.channel

    # we do not need stdin.
    stdin.close()
    # indicate that we're not going to write to that channel anymore
    channel.shutdown_write()

    # read stdout/stderr in order to prevent read block hangs
    stdout_chunks = []
    content = stdout.channel.recv(len(stdout.channel.in_buffer))
    log_output_line(content.decode(), end='')
    stdout_chunks.append(content)

    stderr_chunks = []
    #content = stderr.channel.recv(len(stderr.channel.in_buffer))
    #log_output_line(content.decode(), end='')
    #stderr_chunks.append(content)

    # chunked read to prevent stalls
    while not channel.closed or channel.recv_ready() or channel.recv_stderr_ready():
        # stop if channel was closed prematurely, and there is no data in the buffers.
        got_chunk = False
        readq, _, _ = select.select([stdout.channel], [], [])
        for c in readq:
            if c.recv_ready():
                content = stdout.channel.recv(len(c.in_buffer))
                log_output_line(content.decode(), end='')
                stdout_chunks.append(content)
                got_chunk = True
            if c.recv_stderr_ready():
                # make sure to read stderr to prevent stall
                content = stderr.channel.recv_stderr(len(c.in_stderr_buffer))
                log_output_line(content.decode(), end='')
                stderr_chunks.append(content)
                got_chunk = True
        '''
        1) make sure that there are at least 2 cycles with no data in the input
           buffers in order to not exit too early (i.e. cat on a >200k file).
        2) if no data arrived in the last loop, check if we already received the exit code
        3) check if input buffers are empty
        4) exit the loop
        '''
        if (
            not got_chunk
            and stdout.channel.exit_status_ready()
            and not stderr.channel.recv_stderr_ready()
            and not stdout.channel.recv_ready()
        ):
            # indicate that we're not going to read from this channel anymore
            stdout.channel.shutdown_read()
            # close the channel
            stdout.channel.close()
            break    # exit as remote side is finished and our bufferes are empty

    # close all the pseudofiles
    stdout.close()
    stderr.close()

    return Result(
        stdout.channel.recv_exit_status(),
        b''.join(stdout_chunks),
        b''.join(stderr_chunks)
    )
