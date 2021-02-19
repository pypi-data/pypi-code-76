import stat
from typing import Iterable, Optional, Tuple
from pathlib import Path

from curricula.library import process
from curricula.library.files import delete_file, add_mode
from curricula.library.configurable import Configurable
from curricula_grade.grader.task import Error
from curricula_grade.resource import ExecutableFile, File
from curricula_grade.setup import SetupResult
from curricula_grade.common import Runnable

__all__ = (
    "gpp_compile_object",
    "gpp_compile_shared_object",
    "GppObjectSetup",)


def gpp_compile_object(
        source_path: Path,
        *source_paths: Path,
        destination_path: Path,
        gpp_options: Iterable[str] = (),
        timeout: float = None) -> Tuple[SetupResult, Optional[ExecutableFile]]:
    """Build a binary from a single C++ file with G++."""

    destination_path.parent.mkdir(parents=True, exist_ok=True)
    runtime = process.run(
        "g++",
        str(source_path),
        *map(str, source_paths),
        *gpp_options,
        "-o", str(destination_path),
        timeout=timeout)

    error_description = None
    error_traceback = None
    if runtime.raised_exception:
        error_description = f"error invoking compilation of {source_path.parts[-1]}: {runtime.exception.description}"
    elif runtime.timed_out:
        error_description = f"timed out while compiling {source_path.parts[-1]}"
    elif runtime.code != 0:
        if runtime.stderr:
            error_description = "failed to compile"
            error_traceback = runtime.stderr.decode(errors="replace")
        else:
            error_description = "nonzero status code during compilation"
    elif not destination_path.exists():
        error_description = f"build did not produce {destination_path.parts[-1]}"

    # If the build failed
    if error_description is not None:
        error = Error(description=error_description, traceback=error_traceback)
        return SetupResult(passing=False, runtime=runtime.dump(), error=error), None

    # Chmod
    add_mode(destination_path, stat.S_IXOTH)

    # Otherwise
    return SetupResult(passing=True, runtime=runtime.dump()), ExecutableFile(destination_path)


class GppObjectSetup(Configurable, Runnable):
    """Class-based wrapper for gpp_compile_object."""

    source_paths: Iterable[Path]
    destination_path: Path
    gpp_options: Iterable[str]
    timeout: float
    executable_name: str

    result_type = SetupResult

    def __call__(self, resources: dict) -> SetupResult:
        """Run gpp_compile_object."""

        result, executable = gpp_compile_object(
            *self.resolve("source_paths", field_getter_resources=resources),
            destination_path=self.resolve("destination_path", field_getter_resources=resources),
            gpp_options=self.resolve("gpp_options", default=(), field_getter_resources=resources),
            timeout=self.resolve("timeout", default=None, field_getter_resources=resources))
        resources[self.resolve("executable_name", field_getter_resources=resources)] = executable
        return result


def gpp_compile_shared_object(
        harness_path: Path,
        source_paths: Iterable[Path] = (),
        include_paths: Iterable[Path] = (),
        gpp_options: Iterable[str] = (),
        object_path: Path = Path("harness.o"),
        shared_object_path: Path = Path("harness.so"),
        timeout: float = None) -> Tuple[SetupResult, Optional[File]]:
    """Build a shared object file.

    The target path will be listed after an include flag so that
    headers may be imported.
    """

    runtime = process.run(
        "g++", "-Wall", "-c", *gpp_options,
        str(harness_path.absolute()),
        *map(lambda path: f"{path.absolute()}", source_paths),
        *map(lambda path: f"-I{path.absolute()}", include_paths),
        "-o", str(object_path),
        timeout=timeout)
    if runtime.code != 0 or runtime.raised_exception is not None:
        return (
            SetupResult(
                passing=False,
                runtime=runtime.dump(),
                error=Error(description="compilation failed")),
            None)

    runtime = process.run("g++", "-shared", str(object_path), "-o", str(shared_object_path), timeout=timeout)
    delete_file(object_path)
    if runtime.code != 0 or runtime.raised_exception is not None:
        return (
            SetupResult(
                passing=False,
                runtime=runtime.dump(),
                error=Error(description="shared library build failed")),
            None)

    return SetupResult(passing=True), File(shared_object_path)
