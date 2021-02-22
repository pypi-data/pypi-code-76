import subprocess
from dataclasses import dataclass
from typing import Callable, List, Type

import setuptools
import typer
from dependencies import Injector, value


@dataclass
class FindPackages:
    """Find Python packages in current directory."""

    def __call__(self) -> List[str]:
        """Use Setuptools."""
        return setuptools.find_packages()


@dataclass
class Isort:
    """Format imports with isort."""

    # This attribute is used as command name. FIXME not very usable.
    __name__ = 'isort'

    # FIXME remove this dependency on FindPackages type
    directories: FindPackages

    def __call__(self):
        """Run isort."""
        subprocess.run(['isort', ] + self.directories())


@dataclass
class FlakeHell:
    """Find issues in code with flakehell."""

    __name__ = 'flakehell'

    # FIXME remove this dependency
    directories: FindPackages

    def __call__(self):
        """Run flahekell."""
        subprocess.run(['flakehell', 'lint', ] + self.directories())


@dataclass
class Lint:
    """Check your code."""

    __name__ = 'lint'

    linters: List[Callable[[], None]]

    def __call__(self):
        """Run them all."""
        for linter in self.linters:
            linter()


@dataclass
class Format:
    """Reformat your code."""

    __name__ = 'format'

    formatters: List[Callable[[], None]]

    def __call__(self):
        """Run them all."""
        for formatter in self.formatters:
            formatter()


class Jeeves(Injector):
    """Default Jeeves configuration."""

    # Helpers
    directories = FindPackages

    # Concrete tools
    isort = Isort
    flakehell = FlakeHell

    # Grouped tools
    lint = Lint
    format = Format

    # noinspection PyMethodParameters
    @value
    def linters(flakehell):
        return [flakehell]

    # noinspection PyMethodParameters
    @value
    def formatters(isort):
        return [isort]


def create_app(injector: Type[Injector]):
    """Construct an app and register all commands."""
    app = typer.Typer()

    # Get all registered attributes of the injector class.
    attributes = injector.__dependencies__.specs.keys()

    for attribute in attributes:
        cls = getattr(injector, attribute)
        if hasattr(cls, '__name__'):
            app.command()(cls)

    return app


app = create_app(Jeeves)


if __name__ == '__main__':
    app()
