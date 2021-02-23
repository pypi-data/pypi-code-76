template = '''FROM python:latest

ENV PYTHONBUFFERED=1

RUN pip3 install poetry

WORKDIR /{project_name}

COPY pyproject.toml poetry.lock /test/

RUN poetry config virtualenvs.create false \\
    && poetry install --no-dev

COPY /{project_name} /{project_name}/{project_name}'''
