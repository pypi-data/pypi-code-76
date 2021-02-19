from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

import time
import argparse
import traceback
from threading import Timer
from pathlib import Path
from typing import Optional, Set

from curricula.shell.plugin import Plugin
from curricula.log import log
from curricula_compile import compile
from curricula_compile.compilation import CurriculaTarget
from curricula_compile.exception import CompilationException
from curricula_compile.framework import Configuration
from curricula_compile.validate import validate, validate_problem
from curricula_compile.tools.generate import generate_assignment_interactive, generate_problem_interactive


class TargetHandler(FileSystemEventHandler):
    """Rebuilds when something changes."""

    assignment_path: Path
    target: CurriculaTarget

    paths_modified: Set[Path]
    timer: Optional[Timer]

    def __init__(self, assignment_path: Path, target: CurriculaTarget):
        """Set target."""

        self.assignment_path = assignment_path
        self.target = target
        self.paths_modified = set()
        self.timer = None

    def on_any_event(self, event: FileSystemEvent):
        """Invoked when a file change is detected."""

        if event.is_directory and event.event_type == "modified":
            return
        self.paths_modified.add(Path(event.src_path))

        if self.timer is not None and self.timer.is_alive():
            self.timer.cancel()
        self.timer = Timer(1, self.compile)
        self.timer.start()

    def compile(self):
        """Rebuild with the src_path as modified."""

        log.debug(f"""recompiling for change to {",".join(p.parts[-1] for p in self.paths_modified)}""")

        try:
            self.target.compile(paths_modified=self.paths_modified)
        except CompilationException as exception:
            log.error(exception.message)
        except Exception:
            traceback.print_exc()

        self.paths_modified.clear()
        log.debug(f"waiting for changes...")


class CompilePlugin(Plugin):
    """Plugin for the build subsystem."""

    name = "compile"
    help = "Run the material builder"

    def setup(self, parser: argparse.ArgumentParser):
        """Create a subparser for the build app."""

        parser.add_argument("assignment", help="path to the assignment directory")
        parser.add_argument("problem", help="relative path to a problem", nargs="?")
        command_group = parser.add_mutually_exclusive_group()
        command_group.add_argument(
            "-g", "--generate",
            action="store_true",
            help="generate an assignment or problem")
        command_group.add_argument(
            "-c", "--check",
            action="store_true",
            help="only check JSON manifests")

        command_main_group = command_group.add_argument_group()
        command_main_group.add_argument(
            "-t", "--template",
            dest="template",
            help="generator template directory")
        command_main_group.add_argument(
            "-s", "--site",
            default=None,
            dest="site",
            help="copy instructions to a site")
        command_main_group.add_argument(
            "-w", "--watch",
            action="store_true",
            help="watch for changes and recompile")

        parser.add_argument("--grade", help="grade solution and report", action="store_true")
        parser.add_argument("--grade-tags", help="tags to pass to grade", nargs="+", dest="tags")
        parser.add_argument("--grade-tasks", help="tasks to pass to grade", nargs="+", dest="tasks")

        # Output
        parser.add_argument("-d", "--destination", help="a directory to write the artifacts to")
        parser.add_argument("-i", "--inside", action="store_true", help="make the artifacts directory in destination")

    def main(self, parser: argparse.ArgumentParser, arguments: dict) -> int:
        """Run if the build app is chosen."""

        arguments.get("app")
        if arguments.get("generate"):
            return self.generate(parser, arguments)
        elif arguments.get("check"):
            return self.check(parser, arguments)
        return self.compile(parser, arguments)

    @classmethod
    def compile(cls, parser: argparse.ArgumentParser, options: dict) -> int:
        """Build an assignment."""

        if options["problem"]:
            parser.error("problems may not be built individually")
            return 1

        assignment_path = Path(options.get("assignment")).absolute()
        custom_template_path = Path(options.get("template")) if options["template"] is not None else None

        # Sanity check
        if not assignment_path.is_dir():
            parser.error("assignment path does not exist!")
            return 1

        # If no explicit destination, put inside a custom artifacts directory
        if options["destination"]:
            artifacts_path = Path(options.get("destination")).absolute()
        else:
            artifacts_path = Path().joinpath("artifacts", assignment_path.parts[-1]).absolute()
            options.get("destination")

        # Nest inside directory if flagged
        if options.get("inside"):
            artifacts_path = artifacts_path.joinpath(assignment_path.parts[-1]).absolute()

        # Validate the assignment and build
        kwargs = dict(
            assignment_path=assignment_path,
            artifacts_path=artifacts_path,
            custom_template_path=custom_template_path,
            options=options)
        cls.compile_once(**kwargs)

        if options.get("watch"):
            cls.compile_watch(**kwargs)

        return 0

    @classmethod
    def compile_once(cls, assignment_path: Path, artifacts_path: Path, custom_template_path: Path, options: dict):
        """Normal compilation."""

        validate(assignment_path)
        compile(
            assignment_path=assignment_path,
            artifacts_path=artifacts_path,
            custom_template_path=custom_template_path,
            options=options)

    @classmethod
    def compile_watch(cls, assignment_path: Path, artifacts_path: Path, custom_template_path: Path, options: dict):
        """Compile once and watch for changes."""

        configuration = Configuration(
            assignment_path=assignment_path,
            artifacts_path=artifacts_path,
            custom_template_path=custom_template_path,
            options=options)
        target = CurriculaTarget(configuration)

        observer = Observer()
        observer.schedule(TargetHandler(assignment_path, target), str(assignment_path), recursive=True)
        observer.start()
        log.debug(f"waiting for changes...")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()

        observer.join()

    @classmethod
    def check(cls, parser: argparse.ArgumentParser, options: dict) -> int:
        """Check an assignment."""

        assignment_path = Path(options.get("assignment"))
        if not assignment_path.is_dir():
            parser.error(f"{assignment_path} is not a directory!")
            return 1

        if options["problem"]:
            problem_relative_path = Path(options.get("problem"))
            problem_path = assignment_path.joinpath(problem_relative_path)
            if not problem_path.is_dir():
                parser.error(f"{problem_path} does not exist!")
                return 1

            validate_problem(problem_path)
            return 0

        else:
            validate(assignment_path)
            return 0

    @classmethod
    def generate(cls, parser: argparse.ArgumentParser, options: dict) -> int:
        """Generate a problem or assignment."""

        assignment_path = Path(options.get("assignment"))

        if options["problem"]:
            if not assignment_path.is_dir():
                parser.error("assignment path does not exist!")
                return 1

            problem_relative_path = Path(options.get("problem"))
            generate_problem_interactive(assignment_path, problem_relative_path)
            return 0

        else:
            generate_assignment_interactive(assignment_path)
            return 0
