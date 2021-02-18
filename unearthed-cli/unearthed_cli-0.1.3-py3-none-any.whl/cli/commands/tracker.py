"""Unearthed Tracker command."""
import json
import os
import webbrowser

import click
from unearthed.cli.errors import bail
from unearthed.cli.config import TRACKER_BASE_URL

curr_dir = os.getcwd()


@click.command()
def tracker():
    """Open Unearthed submission tracker."""

    sub_path = os.path.join(os.getcwd(), ".unearthed_last_submission.json")
    if not os.path.exists(sub_path):
        return click.echo(
            'No submissions found in this directory, try "unearthed submit".'
        )
    with open(sub_path) as json_file:
        sub_res = json.load(json_file)

    # Read in the saved challenge details from when `unearthed new` was run
    challenge_path = os.path.join(os.getcwd(), ".unearthed_challenge.json")
    if not os.path.exists(challenge_path):
        return click.echo("No challenge template found in this directory.")
    try:
        with open(challenge_path) as json_file:
            challenge = json.load(json_file)
    except json.decoder.JSONDecodeError as e:
        bail(
            e,
            "There was a problem decoding the challenge template {}.".format(
                challenge_path
            ),
        )

    # Open Tracker
    tracker_url = "{}/crowdml/tracker/{}".format(
        TRACKER_BASE_URL, sub_res["innovatorPortalSubmissionRef"]
    )
    click.echo(
        "You can track the progress of your last submission at: {}".format(tracker_url)
    )
    webbrowser.open_new_tab(tracker_url)
