import subprocess
from pathlib import Path

from fpv_stack.templates.docker_compose import (
    template as dc_template,
)
from fpv_stack.templates.docker_file import (
    template as dockerfile_template,
)
from fpv_stack.templates.main import (
    template as main_template,
)


class ProjectCreator:
    DEPS = ['fastapi[all]']
    DEV_DEPS = ['flake8-mypy']

    def __init__(self, project_name: str):
        self.project_name: str = project_name
        self.project_dir: Path = Path.cwd() / project_name

    def poetry(self) -> None:
        subprocess.run(['poetry', 'new', self.project_name])
        # Add deps
        subprocess.run(
            ['poetry', 'add'] + self.DEPS,
            cwd=self.project_dir.absolute(),
        )
        # Add dev deps
        subprocess.run(
            ['poetry', 'add', '-D'] + self.DEV_DEPS,
            cwd=self.project_dir.absolute(),
        )

        # Add scripts directly to poetry config
        conf = self.project_dir / 'pyproject.toml'
        with conf.open('a', encoding='utf-8') as f:
            f.write(
                '\n[tool.poetry.scripts]\n'
                f'start_dev = "{self.project_name}.main:start_dev"'
            )

    def create_dockerfiles(self) -> None:
        dockerfile = self.project_dir / 'Dockerfile'
        docker_compose = self.project_dir / 'docker-compose.yml'

        with dockerfile.open('w', encoding='utf-8') as f:
            f.write(dockerfile_template.format(project_name=self.project_name))

        with docker_compose.open('w', encoding='utf-8') as f:
            f.write(dc_template.format(project_name=self.project_name))

    def create_python_code(self) -> None:
        app_dir = self.project_dir / self.project_name
        main_file = app_dir / 'main.py'
        with main_file.open('w', encoding='utf-8') as f:
            f.write(main_template.format(project_name=self.project_name))

    def create(self) -> None:
        self.poetry()
        self.create_dockerfiles()
        self.create_python_code()
