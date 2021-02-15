from typing import Optional

class CommandFailed(Exception):
    def __init__(self, cmd, stdout: Optional[bytes], stderr: Optional[bytes]):
        self.cmd = cmd
        self.stdout = stdout
        self.stderr = stderr
