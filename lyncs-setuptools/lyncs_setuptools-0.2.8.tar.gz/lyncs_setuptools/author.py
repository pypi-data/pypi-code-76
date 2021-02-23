"""
Functions for getting the author
"""

__all__ = [
    "find_download_url",
    "find_author",
    "find_email",
]


from git import Git, Repo, GitCommandError


def is_git(directory=None):
    "Returns if the directory (None=cwd) is a git repository"
    try:
        Git(directory).status()
        return True
    except GitCommandError:
        return False


def get_git_repo(directory=None):
    "Returns the git repository in the directory (None=cwd)"
    if Git(directory).rev_parse(is_shallow_repository=True) == "true":
        Git(directory).fetch(unshallow=True)
    return Repo(Git(directory).rev_parse(show_toplevel=True))


def get_git_remote(directory=None):
    "Returns the remote of git repository in the directory (None=cwd)"
    return get_git_repo(directory).remote()


def get_git_branch(branch, directory=None):
    "Returns the master of the git repository in the directory (None=cwd)"
    if not branch in get_git_repo(directory).heads:
        Git(directory).fetch("origin", branch)
    return get_git_repo(directory).heads[branch]


def get_git_author(directory=None):
    "Returns the author of the first git commit"
    *_, commit = get_git_repo(directory).iter_commits()
    return commit.author


def find_download_url():
    "Returns the download url"
    if is_git():
        return next(get_git_remote().urls)
    return None


def find_author():
    "Returns the author name"
    if is_git():
        return get_git_author().name
    return None


def find_email():
    "Returns the author email"
    if is_git():
        return get_git_author().email
    return None
