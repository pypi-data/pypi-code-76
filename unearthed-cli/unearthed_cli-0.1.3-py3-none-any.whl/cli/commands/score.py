"""Preprocessing."""
import logging
import os
from os import makedirs
from os.path import join

import click
import docker
from unearthed.cli.docker import image_exists, pull_image
from unearthed.cli.util import get_challenge

logger = logging.getLogger(__name__)


@click.command()
def score():
    """Run the preprocess step in a local SageMaker container."""
    logger.debug("preprocess")
    challenge = get_challenge()

    # TODO need to push the image to our ECR
    if not image_exists(challenge.dockerImage):
        logger.debug("image not found")
        logger.debug(f"pulling {challenge.dockerImage}")
        pull_image(challenge.dockerImage)

    # create a docker client
    client = docker.from_env()

    # setup docker environment
    env = []
    makedirs(join(os.getcwd(), "data", "scores"), exist_ok=True)
    volumes = {
        os.getcwd(): {"bind": "/opt/ml/code/", "mode": "rw"},
        join(os.getcwd(), "data"): {
            "bind": "/opt/ml/processing/input",
            "mode": "rw",
        },
        join(os.getcwd(), "data", "predictions"): {
            "bind": "/opt/ml/processing/input/predictions",
            "mode": "rw",
        },
        join(os.getcwd(), "data", "scores"): {
            "bind": "/opt/ml/processing/output/scores",
            "mode": "rw",
        },
    }

    try:
        container = client.containers.run(
            image=challenge.dockerImage,
            volumes=volumes,
            environment=env,
            command=[
                "/bin/bash",
                "-c",
                "pip install -r requirements.txt && python score.py",
            ],
            detach=True,
            working_dir="/opt/ml/code",
        )
        for line in container.logs(stream=True):
            print(line.decode("utf-8"), end="")
    except (Exception) as e:
        print(e)
