import os
import re
import subprocess
import sys


def autodetect():
    """Returns a tuple (user, repo). Tries to parse git remote url and also
    Travis CI environment variable."""
    slug = os.environ.get('TRAVIS_REPO_SLUG')
    if slug:
        user, repo = slug.split('/')
        return user, repo

    try:
        remote = subprocess.check_output("git remote get-url origin".split()).decode()
        match = re.match(r"git@github.com:(.+)\/(.+)\.git", remote)
        if match:
            user, repo = match.groups()
            return user, repo
    except subprocess.CalledProcessError as ex:
        print(ex, file=sys.stderr)

    # autodetect failed
    return None, None
