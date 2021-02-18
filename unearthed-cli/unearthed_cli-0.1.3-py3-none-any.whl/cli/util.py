"""Utility functions."""
import json
import logging
import os
import tarfile
from json import JSONDecodeError
from os import makedirs
from os.path import dirname, join
from shutil import copyfile

import click
import requests
from unearthed.cli.errors import bail
from colorama import Back, Fore, Style
from unearthed.cli.auth import auth_handler
from unearthed.cli.config import LAMBDA_URL
from unearthed.core.models.challenge import CHALLENGE_FILENAME, Challenge

logger = logging.getLogger(__name__)


def get_challenge(path=CHALLENGE_FILENAME, id=None):
    """Get a challenge and handle any parsing errors."""
    logger.debug("get_challenge")
    if id is not None:
        try:
            return Challenge.fromApiById(id)
        except Exception as e:
            raise e

    else:
        try:
            return Challenge.fromJsonFile(path)
        except FileNotFoundError as e:
            bail(e, f"No challenge template found in {os.getcwd()}")
        except JSONDecodeError as e:
            bail(e, f"There was a problem decoding the challenge {path}")


def download_from_s3(url, cache_dir=join(os.getcwd(), ".cache")):
    """Download from an S3 signed URL."""
    logger.debug("download_from_s3")

    # Initiate streaming in the archive from url
    if "AWSAccessKeyId" in url:
        logger.debug(f"requesting {url.split('?')[0]}")
    else:
        logger.debug(f"requestion {url}")
    r = requests.get(url, stream=True)

    if r.status_code < 200 or r.status_code > 299:
        logger.debug(f"received HTTP {r.status_code}")
        print(f"There was an error downloading {url.split('?')[0]}.\n")
        print(f"Please contact Unearthed support.")
        exit()

    # determine a name to use in a local cache area
    filename = url.split("?")[0].split("/")[-1]
    cache_filename = join(cache_dir, ".cache", filename)
    logger.debug(f"local cache filename is {cache_filename}")
    makedirs(dirname(cache_filename), exist_ok=True)

    # Initiate the progress tracker of the stream
    total_size = int(r.headers.get("content-length", 0))
    with click.progressbar(length=total_size, label=filename) as bar:
        with open(cache_filename, "wb") as file:
            for data in r.iter_content(1024):
                bar.update(len(data))
                file.write(data)

    return filename


def load_public_data(challenge: Challenge, target_dir=os.getcwd()):
    """Download the public training data."""
    logger.debug("load_public_data")
    filename = download_from_s3(challenge.publicDataUrl, cache_dir=target_dir)
    makedirs(join(target_dir, "data/public"), exist_ok=True)
    copyfile(
        join(target_dir, ".cache", filename), join(target_dir, "data/public", filename)
    )


def load_archive(url, path, name="archive"):
    """Download and unpack an archive from Unearthed Crowd ML S3 bucket."""
    logger.debug("load_archive")

    # Initiate streaming in the archive from url
    if "AWSAccessKeyId" in url:
        logger.debug(f"requesting {url.split('?')[0]}")
    else:
        logger.debug(f"requestion {url}")
    r = requests.get(url, stream=True)

    if r.status_code < 200 or r.status_code > 299:
        logger.debug(f"received HTTP {r.status_code}")
        print(f"There was an error downloading {url.split('?')[0]}.\n")
        print(f"Please contact Unearthed support.")
        exit()

    # TODO this location is not great for large datasets
    tar_path = os.path.expanduser(f"~/.unearthed/downloads/{name}.tar.gz")
    os.makedirs(os.path.dirname(tar_path), exist_ok=True)

    # Initiate the progress tracker of the stream
    total_size = int(r.headers.get("content-length", 0))
    with click.progressbar(length=total_size, label=name) as bar:
        # Save the archive locally
        with open(tar_path, "wb") as tar_file:
            block_size = 1024
            for data in r.iter_content(block_size):
                bar.update(len(data))
                tar_file.write(data)

    # Open and extract the locally saved archive file
    tar = tarfile.open(tar_path)
    os.makedirs(path, exist_ok=True)
    tar.extractall(path=path)


def check_challenge(challenge: Challenge):
    """Check the dataVersion and notifies the user if their template is out-of-date."""
    logger.debug("check_challenge")
    remote_challenge = Challenge.fromApiById(challenge.challengeId)
    if challenge.dataVersion != remote_challenge.dataVersion:
        click.echo(
            Fore.YELLOW
            + "Notice:"
            + Fore.RESET
            + " A new verion of the challenge data or scoring function has been released."
        )
        click.echo(
            "Please update by running: "
            + Fore.LIGHTRED_EX
            + "unearthed reset"
            + Fore.RESET
        )
