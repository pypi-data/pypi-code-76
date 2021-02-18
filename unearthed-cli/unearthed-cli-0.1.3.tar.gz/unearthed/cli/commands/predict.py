"""Prediction."""
import os
import logging
import click
from os.path import join
from os import makedirs

from unearthed.cli.docker import image_exists, pull_image
from unearthed.cli.util import get_challenge

import docker

logger = logging.getLogger(__name__)


@click.command()
def predict():
    """Run the predict step in a local SageMaker container.

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
    makedirs(join(os.getcwd(), "data", "predictions", "public"), exist_ok=True)
    makedirs(join(os.getcwd(), "data", "predictions", "private"), exist_ok=True)
    volumes = {
        os.getcwd(): {"bind": "/opt/ml/code/", "mode": "rw"},
        join(os.getcwd(), "data", "public"): {
            "bind": "/opt/ml/input/data/training",
            "mode": "rw",
        },
        join(os.getcwd(), "model"): {"bind": "/opt/ml/model", "mode": "rw"},
        join(os.getcwd(), "data/predictions"): {"bind": "/opt/ml/output"},
    }

    try:
        container = client.containers.run(
            image=challenge.dockerImage,
            volumes=volumes,
            command=[
                "/bin/bash",
                "-c",
                "pip install -r requirements.txt && python predict.py",
            ],
            detach=True,
            working_dir="/opt/ml/code",
        )
        for line in container.logs(stream=True):
            print(line.decode("utf-8"), end="")
    except (Exception) as e:
        print(e)
