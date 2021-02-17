import logging
import re
from os import environ as env
from pathlib import Path

logger = logging.getLogger("gimme_db_token")


def create_pgpass(pgpass):
    """If given PGPASS file path does not exist, create the file with correct permissions"""
    if not pgpass.is_file():
        pgpass.touch(mode=0o600)
    return pgpass


def find_pgpass():
    """Returns the path to the PGPASS file.
    PG Reference: https://www.postgresql.org/docs/current/libpq-pgpass.html
    """
    if "PGPASSFILE" in env:
        return create_pgpass(Path(env["PGPASSFILE"]))
    # if no env, use pgpass at home directory
    homepgpass = Path.home() / ".pgpass"
    return create_pgpass(homepgpass)


def read_pgpass():
    path = find_pgpass()
    logger.debug(f"Using PGPASS at {path}")
    return open(path).read(), path


def write_pgpass(path, content):
    with open(path, "w") as f:
        f.write(content)


def update_pgpass_str(pgpass, hosts, access_token):
    for host in hosts:
        newline = f"{host}:*:*:*:{access_token}"
        p = re.compile(fr"{host}:\*:\*:\*:.*")
        pgpass, num_replaces = p.subn(newline, pgpass)
        if num_replaces == 0:
            # match is not found, add line on top
            pgpass = "\n".join((newline, pgpass))
    return pgpass


def update_pgpass(access_token, hosts, silent):
    if not hosts:
        # this will print in silent mode, due to the fact that it is an error message
        print("No sidecar endpoints were received. Did not update the PGPASS file.")
        return
    pgpass, path = read_pgpass()
    newpgpass = update_pgpass_str(pgpass, hosts, access_token)
    write_pgpass(path, newpgpass)
    if not silent:
        print("Updated Postgresql token for the following endpoints: 🎉")
        for endpoint in hosts:
            print(f"- {endpoint}")
        print("")
