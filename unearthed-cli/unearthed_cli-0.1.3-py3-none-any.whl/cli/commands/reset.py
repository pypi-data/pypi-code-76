"""Unearthed Reset."""
import os
import shutil

import click
from unearthed.cli.auth import authorize
from unearthed.cli.util import get_challenge, load_archive, load_public_data


@click.group()
def reset():
    """Reset commands."""
    pass


@reset.command()
@authorize
def data():
    """Reset the data directory."""
    current_challenge = get_challenge()
    challenge = get_challenge(id=current_challenge.challengeId)

    # check we are in a challenge dir!

    data_dir = os.path.join(os.getcwd(), "data")

    click.echo("Loading in data files...")
    if click.confirm(
        f"Remove all files in {data_dir} and re-download from Unearthed?",
        default=False,
        abort=True,
    ):
        shutil.rmtree("data", ignore_errors=True)

    load_public_data(challenge)
    return click.echo("The data directory has been reset.")


@reset.command()
@authorize
def scoring_function():
    """Reset the scoring function."""
    current_challenge = get_challenge()
    challenge = get_challenge(id=current_challenge.challengeId)

    # load in scoring function from archive
    click.echo("Loading in scoring function...")

    if click.confirm(
        f"Remove the score.py in {os.getcwd()} and redownload from Unearthed?",
        default=False,
        abort=True,
    ):
        shutil.rmtree("scoring_function", ignore_errors=True)
        if os.path.exists("score.py"):
            os.remove("score.py")

    load_archive(
        challenge.scoringFunctionUrl, "scoring_function", challenge.slug + "_scoring"
    )

    # move the file
    os.rename("scoring_function/score.py", "score.py")
    shutil.rmtree("scoring_function", ignore_errors=True)
    return click.echo("The scoring_function has been reset.")
