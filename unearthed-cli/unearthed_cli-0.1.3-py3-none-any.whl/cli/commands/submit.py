"""Unearthed Submissions."""
import logging
import os
import webbrowser
from json.decoder import JSONDecodeError

import click
import docker
import requests
from unearthed.cli.errors import bail
from unearthed.cli.auth import authorize
from unearthed.cli.commands.build import build
from unearthed.cli.config import TRACKER_BASE_URL
from unearthed.cli.docker import docker_run
from unearthed.cli.util import check_challenge, get_challenge
from unearthed.core.models.submission import Submission

logger = logging.getLogger("unearthed." + __name__)


@click.command()
@click.option("--tracker/--no-tracker", default=True)
@click.option("--logs/--no-logs", default=False)
@click.option("--check/--no-check", default=True)
@click.pass_context
@authorize
def submit(ctx, tracker, logs, check):
    """Create a new submission and upload source code to Unearthed."""
    logger.debug("submit")
    challenge = get_challenge()

    # Check that the challenge is up-to-date
    if check:
        check_challenge(challenge)

    # Bundle the source code
    click.echo("Building your submission...")
    exit_code = ctx.invoke(build, logs=logs)
    if exit_code != 0:
        return click.echo("Build Failed. Try adding --logs to see the build logs.")

    # Create the submission
    click.echo("Creating submission...")
    try:
        submission = Submission.fromApi(challenge.challengeId)
        logger.debug(f"submission id is {submission.submissionId}")
    except JSONDecodeError as e:
        bail(e, "There was a problem contacting the server. Please try again.")
    except Exception as e:
        bail(e, "There was a problem contacting the server.")

    # make sure the source upload URL is present
    if submission.sourceUploadUrl == "":
        return click.echo("Something went wrong getting upload URL")

    # Upload the config file to S3
    with open("submission.yml", "rb") as data:
        response = requests.put(url=submission.configUploadUrl, data=data, timeout=60)
        response.raise_for_status()

    # Upload the source code to S3
    click.echo("Sending submission...")
    logger.debug(f"sending src.tar.gz to {submission.sourceUploadUrl.split('?')[0]}")
    with open("src.tar.gz", "rb") as data:
        response = requests.put(url=submission.sourceUploadUrl, data=data, timeout=60)
        response.raise_for_status()

    # Open the tracker
    click.echo("Submission complete!")
    tracker_url = (
        f"{TRACKER_BASE_URL}/crowdml/tracker/"
        f"{submission.innovatorPortalSubmissionRef}"
    )
    click.echo(f"You can track the progress of your submission at: {tracker_url}")
    if tracker:
        webbrowser.open_new_tab(tracker_url)
