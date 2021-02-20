import argparse
import logging
import os

import ghm
import ghm.meta as meta


def parse():
    parser = argparse.ArgumentParser(
        prog=meta.NAME,
        description=meta.DESCRIPTION,
        epilog=f"{meta.COPYRIGHT} ({meta.URL})"
    )
    parser.add_argument(
        "path",
        help="path for local mirrors"
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{meta.NAME} {meta.VERSION}"
    )

    auth_group = parser.add_argument_group('authentication')
    default_token = ghm.discover_token()
    token_env = f"(default: ${default_token.env})" if default_token.env else ""
    auth_group.add_argument(
        "-t",
        "--token",
        default=default_token.val,
        help=f"github access token {token_env}"
    )

    discovery_group = parser.add_argument_group('repository discovery')
    discovery_group.add_argument(
        "-u",
        "--user",
        help="discover repositories by username"
    )
    discovery_group.add_argument(
        "-o",
        "--org",
        help="discover repositories by organization"
    )

    filter_group = parser.add_argument_group('repository regexp filtering')
    filter_group.add_argument(
        "--match-owner",
        help="include repositories by owner"
    )
    filter_group.add_argument(
        "--match-repo",
        help="include repositories by name"
    )
    filter_group.add_argument(
        "--exclude-owner",
        help="exclude repositories by owner"
    )
    filter_group.add_argument(
        "--exclude-repo",
        help="exclude repositories by name"
    )
    filter_group.add_argument(
        "--exclude-forks",
        action="store_true",
        help="exclude forks"
    )

    perf_group = parser.add_argument_group('performance')
    default_workers = os.cpu_count()
    perf_group.add_argument(
        "--workers",
        default=default_workers,
        help=f"number of mirror workers to run (default: {default_workers})"
    )

    debug_group = parser.add_argument_group('debugging')
    default_log = "info"
    debug_group.add_argument(
        "-l",
        "--log-level",
        choices=("debug", "info", "warning", "error", "critical"),
        default=default_log,
        help=f"show messages of this level or higher (default: {default_log})"
    )
    debug_group.add_argument(
        "--dry-run",
        action="store_true",
        help="show what will happen without making changes"
    )

    options = parser.parse_args()

    if options.dry_run:
        log_format = "[%(levelname)s] (DRY-RUN) %(message)s"
    else:
        log_format = "[%(levelname)s] %(message)s"

    log_level = getattr(logging, options.log_level.upper())
    logging.basicConfig(format=log_format, level=log_level)

    return options
