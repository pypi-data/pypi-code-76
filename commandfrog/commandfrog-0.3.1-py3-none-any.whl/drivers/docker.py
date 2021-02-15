from io import StringIO
import os
import shlex
import subprocess
import tempfile
from typing import Optional, Union

from loguru import logger

from commandfrog.config import Config
from commandfrog.drivers.driver import Driver
from commandfrog.operations.files import directory
from commandfrog.utils import set_env

from .util import execute_command


class DockerHost(Driver):
    has_sudo = False

    container_id: Optional[str]

    def __init__(self, config: Config, image_id: Optional[str] = None, container_id: Optional[str] = None):
        super().__init__(config=config)

        self.image_id = image_id

        assert (image_id is not None) ^ (container_id is not None)

        if image_id is not None:
            self.container_id = subprocess.run(
                f'docker run -d {image_id} tail -f /dev/null',
                shell=True,
                stdout=subprocess.PIPE
            ).stdout.decode().splitlines()[-1]
        else:
            self.container_id = container_id

    def put(self, path: str, contents: Union[str, bytes, StringIO], mode: Optional[Union[str, int]] = None):
        if "~" in path:
            # If we have a tilde in the path, expand it to an absolute path
            # using os.path.expanduser. But that function doesn't give you a
            # direct way of saying what the user's home directory should be,
            # except for setting the `HOME` environment variable, so we do
            # that. We take the HOME environment variable from the container
            # and use it while calling `os.path.expanduser`.
            home_dir = self.base_exec("echo $HOME", echo_stdout=False).stdout.decode().strip()
            with set_env(HOME=home_dir):
                path = os.path.expanduser(path)

        directory(self, os.path.dirname(path))
        with tempfile.NamedTemporaryFile() as fp:
            if isinstance(contents, str):
                bytes = contents.encode()
            elif isinstance(contents, StringIO):
                bytes = contents.getvalue().encode()
            else:
                bytes = contents
            fp.write(bytes)
            fp.seek(0)
            cmd = f"docker cp {fp.name} {self.container_id}:{path}"
            logger.debug("Executing command: {}", cmd)
            subprocess.run(cmd, shell=True, check=True)
            if mode is not None:
                self.exec(f"chmod {mode} {path}")

    def base_exec(
        self,
        cmd: str,
        assert_ok: bool = True,
        echo_stdout: bool = True,
        echo_stderr: bool = True,
    ):
        if self.container_id is None:
            raise ValueError("...")
        cmd = f"docker exec {self.container_id} sh -c {shlex.quote(cmd)}"
        return execute_command(
            cmd,
            echo_stdout=echo_stdout,
            echo_stderr=echo_stderr,
            assert_ok=assert_ok
        )

    def commit(self) -> str:
        """
        Run `docker commit`, return the new image ID.
        """
        proc = subprocess.run(f"docker commit {self.container_id}", stdout=subprocess.PIPE, shell=True)
        return proc.stdout.decode().strip().split(":")[1]

    def disconnect(self) -> str:
        return self.commit()



