from pathlib import Path
from typing import List

from flake8 import defaults
from flake8.api import legacy as flake8
from flake8.formatting.base import BaseFormatter
from flake8.style_guide import Violation

from ..config import Config
from .base import Linter


class Formatter(BaseFormatter):
    errors: List[str] = None

    def after_init(self):
        Formatter.errors = []

    def format(self, error: Violation) -> str:
        return (
            f'{error.filename}:{error.line_number}:{error.column_number}'
            f': {error.code} {error.text}'
        )

    def write(self, line: str, source: str):
        Formatter.errors.append(line)


class Flake8Linter(Linter):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.config = {
            'max_line_length': config.line_length,
        }
        self.config['exclude'] = config.exclude or defaults.EXCLUDE

    def run(self, paths: List[Path]) -> List[str]:
        style_guide = flake8.get_style_guide(**self.config)
        style_guide.init_report(Formatter)
        style_guide.check_files(paths)
        return Formatter.errors

    def dump_config(self, dst: Path) -> None:
        with open(dst / '.flake8', 'w') as out:
            out.write('[flake8]\n')
            out.write(f'max-line-length = {self.config["max_line_length"]}\n')
            out.write(f'exclude = {",".join(self.config["exclude"])}\n')

    @property
    def name(self):
        return 'flake8'
