#!/usr/bin/env python3

import argparse
import glob
import hashlib
import io
import itertools
import logging
import os
import sys
from _hashlib import HASH
from pathlib import Path
from typing import Union, Iterable, List, Optional

from functional import seq

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))


def parse_args(args: List[str]) -> argparse.Namespace:
    """
    Parse the command line arguments.

    :return: The namespace of the parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Compute SHA1 message digest of the given paths. "
            "The output is a combined hash that is the result "
            "of combining all intermediate hashes in a deterministic way (using XOR). "
        )
    )
    parser.add_argument(
        "paths",
        type=str,
        nargs="+",
        action="store",
        help=(
            "One or more paths hash. Paths can include glob patterns, "
            " and can be surrounded with single/double quotes to prevent expansion by the terminal"
        ),
    )
    return parser.parse_args(args)


def _sha1_update_from_file(filename: Union[str, Path], hash_fun: HASH) -> HASH:
    """
    Compute the SHA1 update for a given file.

    :param filename: filename
    :param hash_fun: hash function
    :return: The hash update of the file
    """
    assert Path(filename).is_file()
    b = bytearray(128 * 1024)
    mv = memoryview(b)
    with open(filename, "rb", buffering=0) as f:
        f: io.FileIO
        # Read bytes until there is nothing left to read
        for n in iter(lambda: f.readinto(mv), 0):
            hash_fun.update(mv[:n])
    return hash_fun


def sha1_file(filename: Union[str, Path]) -> str:
    """
    Compute the SHA1 digest of a file.

    :param filename: filename
    :return: The SHA1 digest of the filename
    """
    return str(_sha1_update_from_file(filename, hashlib.sha1()).hexdigest())


def sha_digest(paths: Iterable[Path]) -> int:
    hash_digest = 0
    for path in paths:
        if path.is_file():
            # Take full path and content into account
            filename_digest = int(hashlib.sha1(str(path).encode()).hexdigest(), base=16)
            file_digest = int(sha1_file(path), base=16)
            hash_digest ^= filename_digest ^ file_digest

        else:
            # Invalid path
            logger.warning(f"Skipping unsupported path: {path}")

    return hash_digest


def rel_path(path: Path, other: Path) -> Path:
    """
    Compute the relative path for a path, given another path.

    :param path: Path to compute the relative path for
    :param other: Path from which the relative paths is computed
    :return The relative path to the provided path, with respect to the other path.
    """
    if other.is_file():
        relative_path = os.path.relpath(path, other.parent)
        return Path(relative_path)
    return Path(os.path.relpath(path, other))


def resolve_path(p: Path) -> Optional[Path]:
    try:
        return p.resolve(strict=True)
    except (FileNotFoundError, RuntimeError):
        logger.warning(f"Unable to resolve path: {p}")
        return None


def calculate_hash(paths):
    logger.info(f"Current working directory: {os.getcwd()}")

    logger.info("Raw paths:")
    for path in paths:
        logger.info(f"\t{path}")

    paths_to_hash = (
        seq(paths)
        # Remove surrounding quotes (if any)
        .map(lambda x: x.strip('"').strip("'"))
        # Expand environment variables (if any)
        .map(lambda x: os.path.expandvars(x))
        # Expand glob patterns (if any)
        .map(lambda x: glob.glob(x, recursive=True))
    )

    # Flatten list
    paths_to_hash = list(itertools.chain(*paths_to_hash))

    paths_to_hash = (
        seq(paths_to_hash)
        # Create Path object
        .map(lambda x: Path(x))
        # Filer based resolvable paths
        .filter(lambda x: resolve_path(x) is not None)
        # Make path absolute and resolve any symlink
        .map(lambda x: x.resolve(strict=True))
        # Filter out directories
        .filter(lambda x: not x.is_dir())
        # Relativize with respect to current working directory
        .map(lambda x: rel_path(x, Path.cwd()))
    )

    # Remove duplicates
    paths_to_hash = set(paths_to_hash)

    # Compute combined hash
    combined_hash = hex(sha_digest(paths_to_hash))

    logger.info("Effective hashed paths:")
    for hashed_path in sorted(paths_to_hash):
        logger.info(f"\t{hashed_path}")

    logger.info(f"Combined hash: {combined_hash}")
    return combined_hash


def main():
    args = parse_args(sys.argv[1:])
    h = calculate_hash(args.paths)
    print(h.lstrip("0x"))


if __name__ == "__main__":
    main()
