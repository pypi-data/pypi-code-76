# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
from __future__ import absolute_import

from ..import skipif_extension_not_available
from .testhelpers import (
    HgGitRepoWrapper,
    RepoWrapper,
)


@skipif_extension_not_available('hggit')
def test_export(tmpdir):
    wrapper = RepoWrapper.init(tmpdir / 'repo.hg')
    ctx_default = wrapper.commit_file('foo', message='in default')
    ctx_other = wrapper.commit_file('foo', message="in other", branch='other')

    handler = wrapper.git_handler
    handler.export_commits()
    git_default_sha = handler.map_git_get(ctx_default.hex())
    git_other_sha = handler.map_git_get(ctx_other.hex())

    git_repo = wrapper.inner_git_repo
    assert git_repo.commit_title(git_default_sha) == b'in default'
    assert git_repo.commit_title(git_other_sha) == b'in other'


@skipif_extension_not_available('hggit')
def test_push(tmpdir):
    wrapper = HgGitRepoWrapper.init(tmpdir / 'repo.hg', tmpdir / 'repo.git')

    ctx_dev = wrapper.hg.commit_file('foo', message='in default')
    ctx_bouc = wrapper.hg.commit_file('foo', message="bookmarked")
    wrapper.hg.command('bookmark', b'bouc')
    wrapper.hg.command('bookmark', b'development', rev=ctx_dev.hex())

    wrapper.push()

    handler = wrapper.git_handler
    git_dev_sha = handler.map_git_get(ctx_dev.hex())
    git_bouc_sha = handler.map_git_get(ctx_bouc.hex())

    assert wrapper.git_repo.branches() == {
        b'development': dict(sha=git_dev_sha, title=b'in default'),
        b'bouc': dict(sha=git_bouc_sha, title=b'bookmarked'),
    }
