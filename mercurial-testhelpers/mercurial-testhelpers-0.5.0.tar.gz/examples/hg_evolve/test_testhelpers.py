# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
from __future__ import absolute_import
from mercurial import (
    error,
)
import pytest

from ..import skipif_extension_not_available
from .testhelpers import RepoWrapper


@skipif_extension_not_available('evolve')
def test_prune_update_hidden(tmpdir):
    wrapper = RepoWrapper.init(tmpdir,
                               config=dict(extensions=dict(evolve='')))
    wrapper.commit_file('foo', content='Foo 0')
    ctx = wrapper.commit_file('foo', content='Foo 1', return_ctx=True)
    wrapper.prune('.')
    assert ctx.obsolete()

    wrapper.update(0)
    assert tmpdir.join('foo').read() == 'Foo 0'

    with pytest.raises(error.FilteredRepoLookupError):
        wrapper.update(ctx.hex())

    wrapper.update_bin(ctx.node(), hidden=True)
    assert tmpdir.join('foo').read() == 'Foo 1'


@skipif_extension_not_available('topic')
@skipif_extension_not_available('rebase')
def test_topic(tmpdir):
    """Demonstrate the use of commit_file with parent and topic"""
    # it is essential to activate the rebase extension, even though
    # we don't use it in this test, because the
    # first loading of topic patches it only if it is present.
    # without this, all subsequent tests expecting rebase to preserve
    # topics would be broken
    # TODO add a test with rebase, then
    wrapper = RepoWrapper.init(tmpdir,
                               config=dict(extensions=dict(rebase='',
                                                           topic='')))

    ctx0 = wrapper.commit_file('foo')
    ctx1 = wrapper.commit_file('foo')
    ctx_top = wrapper.commit_file('bar', parent=ctx0, topic='sometop')

    assert ctx_top.topic() == b'sometop'
    assert ctx_top.parents() == [ctx0]

    wrapper.command('rebase', rev=[b'sometop'], dest=b'default')
    repo = wrapper.repo
    rebased_revno = repo.revs(b'sometop').first()
    rebased_ctx = repo[rebased_revno]

    # rebase worked and kept the topic
    assert rebased_ctx.topic() == b'sometop'
    assert rebased_ctx.parents() == [ctx1]

    # topic vanishes upon publication
    wrapper.set_phase('public', ['.'])
    assert not rebased_ctx.topic()

    # reforcing as draft makes it reappear
    wrapper.set_phase('draft', ['.'], force=True)
    assert rebased_ctx.topic() == b'sometop'
