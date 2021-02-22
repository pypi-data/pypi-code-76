import subprocess  # noqa: S404


class Subprocess:
    """Base class for a shell command with specified arguments."""

    def run(self, *args: str):
        """Run a subprocess with given arguments."""
        subprocess.run(args)   # noqa: S603
