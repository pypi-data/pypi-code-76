from typing import Iterable
from pathlib import Path

from curricula.library import process
from curricula_grade.grader.task import Error
from curricula_grade.setup import SetupResult

__all__ = (
    "check_makefile_exists",
    "makefile_execute",)


def check_makefile_exists(path: Path) -> SetupResult:
    """Check whether there is a makefile in a directory."""

    lower_path = path.joinpath("makefile")
    upper_path = path.joinpath("Makefile")

    if not lower_path.exists() and not upper_path.exists():
        return SetupResult(passing=False, error=Error(description=f"can't find {upper_path.parts[-1]}"))
    return SetupResult(passing=True)


def makefile_execute(
        target_path: Path,
        make_options: Iterable[str] = (),
        timeout: float = None) -> SetupResult:
    """Run make on the target directory."""

    runtime = process.run("make", "-B", "-C", str(target_path), *make_options, timeout=timeout)
    if runtime.code != 0 or runtime.timed_out:
        error = f"failed to make {target_path.parts[-1]}"
        return SetupResult(passing=False, error=Error(description=error), runtime=runtime.dump())
    return SetupResult(passing=True, runtime=runtime.dump())
