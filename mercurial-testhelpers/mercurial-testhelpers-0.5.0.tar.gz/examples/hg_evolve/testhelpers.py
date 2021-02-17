# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
"""Compatibility layer for externalisation of testhelpers."""

from mercurial_testhelpers import (  # noqa: F401
    RepoWrapper as CoreRepoWrapper,
    as_bytes,
    make_ui,
)


class RepoWrapper(CoreRepoWrapper):

    def prune(self, revs, successors=(), bookmarks=()):
        # the prune command expects to get all these arguments (it relies
        # on the CLI defaults but doesn't have any at the function call level).
        # They are unconditionally concatened to lists, hence must be lists.
        # (as of Mercurial 5.3.1)
        if isinstance(revs, (bytes, str)):
            revs = [revs]
        return self.command('prune',
                            rev=[as_bytes(r) for r in revs],
                            new=[],  # deprecated yet expected
                            # TODO py3 convert these two to bytes as needed:
                            successor=list(successors),
                            bookmark=list(bookmarks))

    def set_topic(self, topic):
        self.command('topics', as_bytes(topic))

RepoWrapper.register_commit_option('topic', 'set_topic')
