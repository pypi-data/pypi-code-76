"""
process utilities
"""
import typing
import shlex
import subprocess
import logging


def execute(
    system_command: str,
    level: typing.Optional[int] = None,
    logger: typing.Optional[typing.Union[logging.Logger, bool]] = None,
    output: bool = False,
    **kwargs
) -> typing.Optional[typing.List[str]]:
    """
    Execute a system command, passing STDOUT and STDERR to logger.

    Args:
        system_command: code to execute
        level: logging level of the message (not of the logger). Defaults to DEBUG
        logger: if not None, log the command an also automaticaly infer output = True.
            if logger==True create a logger from the name
        output: if True, return the output. Is False by default because communicate can
            eventually overflow the memory buffer. If False returns None
        **kwargs: forwarded to Popen

    Examples:
        >>> import rna
        >>> import logging
        >>> log = logging.getLogger(__name__)

        Returns the output if ....

        ... any logging is involved
        >>> rna.process.execute("echo 'Test'", level=logging.ERROR)
        ['Test']
        >>> rna.process.execute("echo 'Test'", logger=log)
        ['Test']

        ... or explicitly asked for
        >>> rna.process.execute("echo 'Test'", level=None, output=True)
        ['Test']

        To be more efficient
        >>> rna.process.execute("echo 'Test'", level=None)

    """
    if level is not None and logger is None:
        logger = True
    if logger and isinstance(logger, bool):  # i.e. True
        logger = logging.Logger("Output of {}".format(system_command))
    if logger or output:
        if level is None:
            level = logging.DEBUG
        kwargs.setdefault("text", True)
        kwargs.setdefault("stdout", subprocess.PIPE)
        kwargs.setdefault("stderr", subprocess.STDOUT)
    if logger:
        logger.log(level, "Executing system command: '%s'", system_command)
    pipe = subprocess.Popen(shlex.split(system_command), **kwargs)
    if logger:
        out = []
        for line in iter(pipe.stdout.readline, ""):
            line = line.strip("\n")
            logging.log(level, line)
            out.append(line)
        pipe.stdout.close()
        return_code = pipe.wait()
    elif output:
        out, return_code = pipe.communicate()
        out = out.rstrip("\n").split("\n")
    else:
        out = None
        return_code = pipe.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, system_command)
    return out
