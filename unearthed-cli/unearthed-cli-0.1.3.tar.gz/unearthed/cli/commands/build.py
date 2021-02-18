"""Build command."""
import logging
import os

import click
from unearthed.cli.docker import docker_run
from unearthed.cli.util import get_challenge

logger = logging.getLogger(__name__)


@click.command()
@click.option("--logs/--no-logs", default=True)
def build(logs):
    """Build the submission files using docker and setuptools."""
    logger.debug("build")
    logger.info("Building your submission")

    challenge = get_challenge(".unearthed_challenge.json")

    # the original build sequence uses:
    # - a build step in a Makefile
    #   - (redundantly) installs requirements.txt
    #   - runs setuptools sdist
    #   - renames the resulting package to src.tar.gz
    # - an unpack step in the consuming Makefile
    #   - flattens the python sdist tarball
    #
    # template Makefile
    # requirements:
    #     cat requirements.txt
    #     $(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel python-dotenv click Sphinx coverage flake8 --quiet || echo "Skipping failed pip install"
    #     # Ensure requirements.txt exists.
    #     cat requirements.txt
    #     $(PYTHON_INTERPRETER) -m pip install -r requirements.txt --quiet || echo "Skipping failed pip install"
    # build:requirements
    # 	rm -rf dist build *.egg-info
    # 	$(PYTHON_INTERPRETER) setup.py sdist bdist_wheel
    # 	cp dist/*.tar.gz dist/src.tar.gz
    #
    # Scoring Makefilecontainer_setup_predict:
    # container_setup_predict:
    # 	# load and unpack model source
    # 	wget -qO- "$(SOURCE_URL)" | tar xz --strip-components=1

    volumes = {os.getcwd(): {"bind": "/tmp/unearthed", "mode": "rw"}}

    # consider setup.py -q to quieten
    cmd = (
        "/bin/bash -c '"
        "cd /tmp/unearthed && python setup.py sdist &&"
        "tar xzf dist/*.tar.gz -C dist --strip-components=1 &&"
        "cd dist && rm -rf *.tar.gz PKG-INFO *.egg-info setup.py setup.cfg pyproject.toml MANIFEST.in &&"
        "tar czf ../src.tar.gz . &&"
        "cd .. && rm -rf dist *.egg-info"
        "'"
    )

    # run setuptools sdist
    result = docker_run(challenge, volumes=volumes, cmd=cmd, logs=logs)
    if result != 1:
        return result
    print(f"build complete")
    return 0
