from typing import Union
import logging
import os
import subprocess
import tempfile

logger = logging.getLogger(__name__)


def run_subprocess(
    *args: tuple,
    check: bool = True,
    stdout_level: int = logging.DEBUG,
    stderr_level: int = logging.DEBUG,
):
    completed_process = subprocess.run(
        args, capture_output=True, text=True, check=False
    )
    if completed_process.stdout:
        logger.log(stdout_level, "stdout: %r", completed_process.stdout)
    if completed_process.stderr:
        logger.log(stderr_level, "stderr: %r", completed_process.stderr)
    if check:
        completed_process.check_returncode()


def cjpeg(
    source: Union[bytes, str, os.PathLike],
    target: Union[bytes, str, os.PathLike],
    quality: Union[int, str] = 75,
    executable: str = "cjpeg",
):
    """
    Recompress jpeg file from `source` to `target` using specified cjpeg implementation.
    """
    run_subprocess(
        executable,
        "-quality",
        str(quality),
        "-outfile",
        target,
        source,
    )


def pngquant(
    source: Union[bytes, str, os.PathLike],
    target: Union[bytes, str, os.PathLike],
    quality: Union[int, str] = 80,
    executable: str = "pngquant",
):
    """
    Recompress png file from `source` to `target`.
    """
    run_subprocess(
        executable,
        "--quality",
        str(quality),
        "--force",
        "--output",
        target,
        "--",
        source,
    )


KINDLEGEN_COMPRESSION = {
    0: "no compression",
    1: "DOC compression",
    2: "Kindle huffdic compression",
}


def kindlegen(
    source: Union[bytes, str, os.PathLike],
    target: Union[bytes, str, os.PathLike],
    compression: int = 1,
    executable: str = "kindlegen",
):
    """
    Convert EPUB (or other kindlegen-compatible input) to Kindle (MOBI) format.
    """
    if compression not in KINDLEGEN_COMPRESSION:
        raise ValueError(
            f"compression={compression} is not a valid option (should be one of {set(KINDLEGEN_COMPRESSION)})"
        )
    # kindlegen is kinda clunky in that it requires the output be in the same directory
    # as the input :( which is consistent with typical usage, but not the general case
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_source = os.path.join(tmpdir, os.path.basename(source))
        os.link(source, tmp_source)
        tmp_target = os.path.join(tmpdir, os.path.basename(target))
        run_subprocess(
            executable,
            tmp_source,
            f"-c{compression}",
            "-o",
            os.path.basename(tmp_target),
        )
        os.rename(tmp_target, target)
