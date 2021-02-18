"""Training."""
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
def train():
    """Run the train step in a local SageMaker container.

    See https://docs.aws.amazon.com/sagemaker/latest/dg/pre-built-docker-containers-scikit-learn-spark.html
    """
    logger.debug("train")
    challenge = get_challenge()

    # TODO need to push the image to our ECR
    if not image_exists(challenge.dockerImage):
        logger.debug("image not found")
        logger.debug(f"pulling {challenge.dockerImage}")
        pull_image(challenge.dockerImage)

    # create a docker client
    client = docker.from_env()

    # setup docker environment
    env = [
        "SM_CHANNEL_TRAINING=/opt/ml/input/data/training",
    ]
    makedirs(join(os.getcwd(), "model"), exist_ok=True)
    volumes = {
        os.getcwd(): {"bind": "/opt/ml/code/", "mode": "rw"},
        join(os.getcwd(), "data", "public"): {
            "bind": "/opt/ml/input/data/training",
            "mode": "rw",
        },
        join(os.getcwd(), "model"): {"bind": "/opt/ml/model", "mode": "rw"},
    }

    try:
        container = client.containers.run(
            image=challenge.dockerImage,
            volumes=volumes,
            environment=env,
            command=[
                "/bin/bash",
                "-c",
                "pip install -r requirements.txt && python train.py",
            ],
            detach=True,
            working_dir="/opt/ml/code",
        )
        for line in container.logs(stream=True):
            print(line.decode("utf-8"), end="")
    except (Exception) as e:
        print(e)
