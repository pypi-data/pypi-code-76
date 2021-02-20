from collections import namedtuple
import github
import logging
import os
import pathlib
import pygit2
import re


log = logging.getLogger(__name__)


def discover_token(envs=["GITHUB_TOKEN"]):
    Token = namedtuple('Token', "env, val")
    for env in envs:
        val = os.environ.get(env)
        if val:
            return Token(env, val)
    return Token(None, None)


def discover_repos(token, user, org):
    repos = []
    if token:
        gh = github.Github(token)
        repos = gh.get_user().get_repos()
    else:
        gh = github.Github()
        if user:
            repos = gh.get_user(user).get_repos()
        elif org:
            repos = gh.get_organization(org).get_repos()

    names = set(r.full_name for r in repos)
    log.debug(f"Discovered {len(names)} repositories: {', '.join(names)}")

    return repos


def filter_repos(repos, match_owner=None, match_repo=None, exclude_owner=None,
                 exclude_repo=None, exclude_forks=False):
    all_repos = set(r.full_name for r in repos)

    if match_owner:
        repos = [r for r in repos if re.search(match_owner, r.owner.login)]
    if match_repo:
        repos = [r for r in repos if re.search(match_repo, r.name)]
    if exclude_owner:
        repos = [r for r in repos
                 if not re.search(exclude_owner, r.owner.login)]
    if exclude_repo:
        repos = [r for r in repos if not re.search(exclude_repo, r.name)]
    if exclude_forks:
        repos = [r for r in repos if not r.fork]

    selected_repos = set(n.full_name for n in repos)
    excluded_repos = sorted(all_repos - selected_repos)
    log.debug(
        f"Excluded {len(excluded_repos)} repositories: " +
        f"{', '.join(excluded_repos)}"
    )
    log.info(
        f"Selected {len(selected_repos)} repositories: " +
        f"{', '.join(selected_repos)}")

    return repos


def clone_path(root, repo):
    return os.path.join(root, repo.owner.login, f"{repo.name}.git")


def mkdir_p(path):
    if os.path.exists(path):
        return False
    pathlib.Path(path).mkdir(parents=True)
    return True


# FIXME: Support SSH authentication
def git_credentials_callback(token=None):
    credentials = pygit2.UserPass(token, "")
    return pygit2.RemoteCallbacks(credentials=credentials)


def git_mirror_remote(repo, name, url):
    remote = repo.remotes.create(name, url, "+refs/*:refs/*")
    repo.config[f"remote.{name}.mirror"] = True
    return remote


# FIXME: Support SSH URLs
def clone_repo(repo, path, callbacks=None, dry_run=False):
    if os.path.isdir(path) and os.listdir(path):
        return False

    url = repo.clone_url
    log.info(f"Clone: {url} -> {path}")
    if dry_run:
        return False

    mkdir_p(path)
    return pygit2.clone_repository(
        url,
        path,
        callbacks=callbacks,
        bare=True,
        remote=git_mirror_remote
    )


def fetch_repo(path, callbacks=None, dry_run=False):
    if not os.path.isdir(path):
        return False

    repo = pygit2.Repository(path)
    remote = repo.remotes["origin"]
    log.info(f"Fetch: {remote.url} -> {path}")
    if dry_run:
        return False

    return remote.fetch(callbacks=callbacks, prune=pygit2.GIT_FETCH_PRUNE)
