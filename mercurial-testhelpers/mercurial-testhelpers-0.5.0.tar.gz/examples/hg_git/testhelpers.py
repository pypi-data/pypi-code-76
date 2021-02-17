# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
"""Helpers for hg-git

This is an over-simple version of what hg-git could provide for its own
purposes and of its downstreams.

This is using the actual `git` executable, arguably providing more
end-to-end testing. Nothing prevents inner tests to be written with dulwich.
"""
from __future__ import absolute_import
import os
import subprocess

from mercurial import (
    pycompat,
)

from mercurial_testhelpers import (
    as_bytes,
    RepoWrapper as CoreRepoWrapper,
)


def as_str(s):
    if isinstance(s, bytes):
        return pycompat.sysstr(s)
    return str(s)  # takes care of various Path instances used by pytest


class GitRepo(object):
    """Represents an actual Git repository on the file system.

    Subset of the `GitRepo` class used in py-heptapod integration tests.
    """

    def __init__(self, path):
        # even if the result is weird if there is a codec mismatch
        # the point of hg-git tests is not to test that Mercurial and
        # Git paths on disk can be arbitrary bytes.
        self.path = as_str(path)

    @classmethod
    def init(cls, path):
        subprocess.call(('git', 'init', '--bare', as_str(path)))
        return cls(path)

    def branches(self):
        out = subprocess.check_output(('git', 'branch', '-v', '--no-abbrev'),
                                      cwd=self.path)
        split_lines = (line.lstrip(b'*').strip().split(None, 2)
                       for line in out.splitlines())
        return {sp[0]: dict(sha=sp[1], title=sp[2]) for sp in split_lines}

    def commit_title(self, revspec):
        out = subprocess.check_output(
            ('git', 'log', '-n1', revspec, r'--pretty=format:%s'),
            cwd=self.path)
        return out.strip()


class RepoWrapper(CoreRepoWrapper):

    def __init__(self, *args, **kwargs):
        super(RepoWrapper, self).__init__(*args, **kwargs)
        self.inner_git_repo = GitRepo(
            os.path.join(self.repo.root, b'.hg', b'git'))
        self._git_handler = None

    @property
    def git_handler(self):
        handler = self._git_handler
        if handler is not None:
            return handler

        # import in-method to be done only if actually in use
        # so that imports aren't broken and skip conditions work
        from hggit.git_handler import GitHandler

        self._git_handler = GitHandler(self.repo, self.repo.ui)
        return self._git_handler


class HgGitRepoWrapper(object):
    """Represent a pair of Mercurial and Git repositories."""

    def __init__(self, hg_wrapper, git_repo):
        self.hg = hg_wrapper
        self.hg_repo = hg_wrapper.repo
        self.git_repo = git_repo

    @property
    def git_handler(self):
        return self.hg.git_handler

    @classmethod
    def init(cls, hg_path, git_path):
        """Create a pair of empty Mercurial and Git repos."""
        return cls(RepoWrapper.init(hg_path), GitRepo.init(git_path))

    def push(self, revs=None, force=False):
        """Push from the Mercurial repo to the Git repo.

        :param revs: if ``None``, means to push everything
        """
        self.git_handler.push(as_bytes(self.git_repo.path),
                              revs=revs, force=force)
