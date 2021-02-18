"""Unearthed New Command."""
import logging
import os
import shutil

import click
from click import Choice
from unearthed.cli.auth import authorize
from unearthed.cli.util import load_archive, load_public_data
from unearthed.core.models.challenge import CHALLENGE_FILENAME, Challenge

logger = logging.getLogger(__name__)


# Prompt the user to select one of the challenges
# Checks if the user provided a challenge slug and load that without prompt
def _get_challenge(challenge_slug) -> Challenge:
    """Get a challenge instance based on challenge_slug."""
    logger.debug("get_challenge")
    challenges = Challenge.allFromApi()

    # if there are no challenges in list just return None
    if len(challenges) == 0:
        return None

    # check to see if the requested challenge slug is in the list of available
    # challenges
    if challenge_slug is not None:
        challenge = next(
            (challenge for challenge in challenges if challenge.slug == challenge_slug),
            None,
        )
        if challenge is not None:
            return challenge

    # otherwise, ask which challenge template is desired
    click.echo("Available challenges:")
    for idx, challenge in enumerate(challenges):
        click.echo(f" [{idx+1}]  {challenge.name} ({challenge.slug})")

    selected = click.prompt(
        "Which challenge template do you wish to download?",
        type=click.IntRange(min=1, max=len(challenges), clamp=False),
    )
    return challenges[selected - 1]


@click.command()
@click.argument(
    "target_dir",
    type=click.Path(exists=False),
    default=os.getcwd(),
)
@click.option("--challenge", type=click.STRING)
@click.option("--data/--no-data", default=True)
@authorize
def new(target_dir, challenge, data):
    """Create a new Unearthed submission project from an S3 template."""
    logger.debug("new")
    challenge = _get_challenge(challenge)
    if challenge is None:
        return click.echo("You are not registered for any competitions.")

    # note challenge is now a Challenge instance
    logger.debug(f"challenge is {challenge.slug}")

    # Build and validate the path for the template
    # TODO this should really check the folder and fail if it exists
    logger.debug(f"parent_dir is {target_dir}")

    # if the target_dir is the current dir, then create a dir from the
    # challenge slug
    if target_dir == os.getcwd():
        target_dir = os.path.join(target_dir, challenge.slug)
    challenge_file = os.path.join(target_dir, CHALLENGE_FILENAME)

    # check to see if the target_dir is empty of not, and if it is not
    # prompt to overwrite
    if os.path.exists(target_dir) and len(os.listdir(target_dir)) != 0:
        click.echo(f"{target_dir} is not empty")
        if click.confirm("Overwrite?", default=False, abort=True):
            shutil.rmtree(target_dir, ignore_errors=True)

    # load in template from archive
    click.echo("Loading in template...")
    load_archive(challenge.templateUrl, target_dir, challenge.slug + "_template")

    # load in scoring function from archive
    click.echo("Loading in scoring function...")
    load_archive(challenge.scoringFunctionUrl, target_dir, challenge.slug + "_scoring")

    # load in data from archive
    if data:
        click.echo("Loading in data files...")
        load_public_data(challenge, target_dir=target_dir)

    # Save the challenge details for later
    challenge.save(filename=challenge_file)
    click.echo(f"Challenge template downloaded and ready to use at {target_dir}")
