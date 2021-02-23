from datetime import datetime
from pathlib import Path

from cookiecutter.main import cookiecutter

from pyquickstart.config import PACKAGE_ROOT


class Project:
    def __init__(self):
        self.template = 'standard'
        self.path = None

    def create(self, no_prompt=False):
        context = {
            'year': datetime.now().year
        }
        template_path = PACKAGE_ROOT / 'templates' / self.template

        result = cookiecutter(
            str(template_path),
            extra_context=context,
            no_input=no_prompt
        )
        self.path = Path(result)
