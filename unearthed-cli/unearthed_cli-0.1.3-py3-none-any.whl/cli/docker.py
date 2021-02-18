"""Docker wrapper."""
import logging

from tqdm import tqdm
from unearthed.cli.errors import bail

import docker
from docker.errors import ImageNotFound, DockerException

logger = logging.getLogger(__name__)


def image_exists(image_name: str) -> bool:
    """Check a docker image exists."""
    logger.debug("image_exists")
    try:
        client = docker.from_env()
        client.images.get(image_name)
        return True
    except ImageNotFound:
        return False
    except DockerException:
        logger.error("could not connect to Docker")
        return False


def pull_image(image_name):
    """Pull a docker image and display a status bar."""
    bars = {}
    pos = 0

    client = docker.from_env()

    for update in client.api.pull(image_name, stream=True, decode=True):
        status = update.get("status", "")
        bar = update.get("id", "")
        progress = update.get("progress", "")
        if bar not in bars:
            bars[bar] = tqdm(position=pos, initial=1, leave=True)
            bars[bar].display("")
            pos += 1
        bars[bar].display(" ".join([bar, status, progress]))

    [bars[bar].close() for bar in bars]


# Abstraction command for running a command in the container
def docker_run(chall, cmd="", env=[], volumes={}, logs=True, pull=False):
    """Run a command in a Docker image."""
    logger.debug("docker_run")
    # TODO probably need to pass the image in from a config
    # it is in the mongo db, not sure if this is the right place for it
    docker_image = "python:3.8-slim"

    logger.info(f"calling docker run -t {docker_image}")
    try:
        # only pull if image does not exist or flag is set
        if pull or not image_exists(docker_image):
            pull_image(docker_image)
    except Exception as e:
        bail(
            e,
            "There was a problem fetching the Docker image.\n"
            "Please make sure you have Docker installed.",
        )

    print("Running command on image " + docker_image)

    # Start the command execution
    client = docker.from_env()
    container = client.containers.run(
        image=docker_image,
        command=cmd,
        # command="bash -c '{}'".format(cmd),
        auto_remove=True,
        volumes=volumes,
        environment=env,
        network_mode="host",
        detach=True,
    )
    # If enabled, output the logs
    logs = True
    if logs:
        log_stream = container.logs(stream=True)
        for line in log_stream:
            print(line.decode("utf-8"), end="")
    # Wait until the container is finished executing
    res = container.wait()
    # Return the exit code of the command
    return res["StatusCode"]
