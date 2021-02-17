# -*- coding: utf-8 -*-
from datetime import datetime
from mercurial import (
    encoding,
    error,
    revset,
    revsetlang,
    util,
)
import pytest
from mercurial_testhelpers import (
    RepoWrapper,
    as_bytes,
)

hg_version = util.versiontuple()


def assert_revset_list(repo, revset, expected):
    assert list(repo.revs(as_bytes(revset))) == expected


def debug_revspec(repo, expr):
    expr = as_bytes(expr)
    aliases = repo.ui.configitems(b'revsetalias')
    tree = revsetlang.parse(expr, lookup=revset.lookupfn(repo))
    stages = [
        (b'parsed', lambda tree: tree),
        (
            b'expanded',
            lambda tree: revsetlang.expandaliases(tree, aliases, repo.ui.warn),
        ),
        (b'concatenated', revsetlang.foldconcat),
        (b'analyzed', revsetlang.analyze),
        (b'optimized', revsetlang.optimize),
    ]
    for _n, f in stages:
        tree = f(tree)
    func = revset.makematcher(tree)
    revs = func(repo)
    return list(revs)


@pytest.mark.skipif(
    hg_version < (5, 4),
    reason="This test is a translation from hg 5.6. As such, it contains "
    "many statements that don't pass in prior versions.")
def test_revset(tmpdir, monkeypatch):
    repo_path = tmpdir.join('repo')
    wrapper = RepoWrapper.init(repo_path,
                               config=dict(ui=dict(username=b'test')))

    repo = wrapper.repo

    ctx0 = wrapper.commit_file('a', content='a', message="0", branch='a')
    ctx1 = wrapper.commit_file('b', content='b', message="1", branch='b')
    # we don't have a wrapper.rm_commit helper
    ctx2 = wrapper.commit_removal('a', branch='a-b-c-', user='Bob')
    assert list(repo.revs(b"extra('branch', 'a-b-c-')")) == [2]
    assert list(repo.revs(b"extra('branch', 're:a')")) == [0, 2]
    ctx3 = wrapper.commit_empty(message="3", parent=ctx1, branch="+a+b+c+")
    ctx4 = wrapper.commit_file(
        'b',
        message="4",
        content='bb',
        branch='-a-b-c-',
        # test-revset.t uses the local timezone. We'll make a small
        # difference here that doesn't matter for the results, because
        # mercurial_testhelpers does not accept local time zones by design.
        utc_datetime=datetime(2005, 5, 12),
        parent=ctx2)
    wrapper.commit_empty(message="5 bug",
                         parent=ctx3,
                         branch="!a/b/c/")
    wrapper.merge_commit(ctx4, message="6 issue619", branch="_a_b_c_")
    wrapper.commit_empty(message="7", branch=".a.b.c.")

    # seems useless but may be a bug reproduction?
    wrapper.command('branch', b'all')

    # using a UTF-8 litteral works out of the box, because that's the
    # codec used by the test helpers.

    # We still need Mercurial to be ready to handle UTF-8.
    # In our current CI jobs, `encoding.encoding` is `ascii`, leading
    # to failure in `encoding.tolocal`. We fix that with the `monkeypatch`
    # builtin fixture of pytest, that makes sure this is reverted at the
    # end of the test.
    # Users may prefer to run the whole suite with HGENCODING=UTF-8,
    # but this here is a good enough way to get independence of context.
    monkeypatch.setattr(encoding, 'encoding', 'utf-8')

    # The explicit form for non-ascii character, also working indifferently
    # for Python 2 and 3 would be u"\xe9".encode('utf-8') or the
    # more direct b"\xc3\xa9"
    wrapper.commit_empty(message="9", parent=ctx4, branch="é")

    # NdGr don't know why ui.username isn't interpreted here
    wrapper.command('tag', b'1.0', rev=b'6', user=b'test')
    wrapper.command('bookmark', b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
                    rev=b'6')

    # trivial cases
    assert_revset_list(repo, '0:1', [0, 1])
    # test-revset.t uses `--optimize`. That seems to be for outputing
    # the parsed tree after optimization (out of scope for this demo then)
    assert_revset_list(repo, ':', list(range(10)))
    assert_revset_list(repo, '3::6', [3, 5, 6])
    assert_revset_list(repo, '0|1|2', [0, 1, 2])

    # names that should work without quoting
    assert_revset_list(repo, 'a', [0])
    assert_revset_list(repo, 'b-a', [1])
    assert_revset_list(repo, '_a_b_c_', [6])
    assert_revset_list(repo, '_a_b_c_-a', [6])
    assert_revset_list(repo, '.a.b.c.', [7])
    assert_revset_list(repo, '.a.b.c.-a', [7])

    # names that should be caught by fallback mechanism
    # NdGR here debug_revspec does something different than repo.revs()
    assert debug_revspec(repo, b'-a-b-c-') == [4]
    assert debug_revspec(repo, b'+a+b+c+') == [3]
    assert debug_revspec(repo, b'+a+b+c+:') == list(range(3, 10))
    assert debug_revspec(repo, b':+a+b+c+') == list(range(4))
    assert debug_revspec(repo, b'-a-b-c-:+a+b+c+') == [4, 3]
    with pytest.raises(error.RepoLookupError) as exc_info:
        debug_revspec(repo, b'-a-b-c--a')
    # NdGR I'm not in favor of testing actual error message content
    assert b"'-a'" in exc_info.value.args[0]
    assert_revset_list(repo, 'é', [9])

    # no quoting needed
    assert debug_revspec(repo, b'::a-b-c-') == [0, 1, 2]

    # quoting needed
    assert_revset_list(repo, '"-a-b-c-"-a', [4])
    assert_revset_list(repo, '1 or 2', [1, 2])
    assert_revset_list(repo, '1|2', [1, 2])
    assert_revset_list(repo, '1&2', [])
    # precedence: & is higher
    assert_revset_list(repo, '1&2|3', [3])
    assert_revset_list(repo, '1|2&3', [1])
    # associativity
    assert_revset_list(repo, '1&2&3', [])
    assert_revset_list(repo, '1|(2|3)', [1, 2, 3])
    # tag
    assert_revset_list(repo, '1.0', [6])
    # branch
    assert_revset_list(repo, 'a', [0])
    assert_revset_list(repo, ctx0.hex()[:10], [0])  # was 2785f51ee
    assert_revset_list(repo, 'date(2005)', [4])

    # date invalid syntaxes
    with pytest.raises(error.ParseError):
        repo.revs('date(this is a test)')
    with pytest.raises(error.ParseError):
        repo.revs('date()')
    with pytest.raises(error.RepoLookupError):
        repo.revs('date')
    with pytest.raises(error.ParseError):
        repo.revs('date(')
    with pytest.raises(error.ParseError):
        repo.revs(r'date("\xy")')
    with pytest.raises(error.ParseError):
        repo.revs('date(tip)')
    with pytest.raises(error.RepoLookupError):
        repo.revs('0:date')
    with pytest.raises(error.RepoLookupError):
        repo.revs('::date')

    wrapper.command('bookmark', b'date', rev=b'4')
    assert_revset_list(repo, '0:date', list(range(5)))
    assert_revset_list(repo, '::date', [0, 1, 2, 4])
    assert_revset_list(repo, '::"date"', [0, 1, 2, 4])
    assert_revset_list(repo, 'date(2005) and 1::', [4])
    wrapper.command('bookmark', b'date', delete=True)

    # function name shoud be a symbol
    with pytest.raises(error.ParseError):
        repo.revs('"date"(2005)')

    # keyword arguments
    assert_revset_list(repo, 'extra(branch, value=a)', [0])
    # TODO should really add assertions to make distinction from my own
    # typos
    with pytest.raises(error.ParseError):
        repo.revs('extra(branch, a, b)')
    with pytest.raises(error.ParseError):
        repo.revs('extra(label=branch, default)')
    with pytest.raises(error.ParseError):
        repo.revs('extra(branch, foo+bar=baz)')
    with pytest.raises(error.ParseError):
        repo.revs('extra(unkown=branch)')
    with pytest.raises(error.ParseError):
        repo.revs('extra((), x)')
    with pytest.raises(error.ParseError):
        repo.revs('extra(label=x, ())')
    with pytest.raises(error.ParseError):
        repo.revs('foo=bar|baz')

    # right-hand side should be optimized recursively
    # TODO not sure what to make of that one. Can the point really be
    # the resulting graph before raising the error ?
    with pytest.raises(error.ParseError):
        repo.revs('foo=(not public())')

    # relation-subscript operator has the highest binding strength
    # (as function call):
    assert_revset_list(repo, 'tip:tip^#generations[-1]', [9, 8, 7, 6, 5, 4])

    # TODO some really about resulting AST and its optim
    # still calling not to cheat on exec times

    # $ hg debugrevspec -p parsed --no-show-revs 'not public()#generations[0]'
    debug_revspec(repo, b'not public()#generations[0]')
    # $ hg debugrevspec -p analyzed -p optimized --no-show-revs \
    #   > '(not public())#generations[0]'
    debug_revspec(repo, b'not public()#generations[0]')

    # TODO again only analysis, have to assert on that
    with pytest.raises(error.ParseError):
        repo.revs('tip[0]')
    with pytest.raises(error.ParseError):
        repo.revs('tip#rel[0]')
    with pytest.raises(error.ParseError):
        repo.revs('(tip#rel)[0]')
    with pytest.raises(error.ParseError):
        repo.revs('tip#rel[0][1]')
    with pytest.raises(error.ParseError):
        repo.revs('tip#rel0#rel1[1]')
    with pytest.raises(error.ParseError):
        repo.revs('tip#rel0[0]#rel1[1]')

    # parse errors of relation, subscript and relation-subscript operators
    # suggested relations
    # parsed tree at stages
    # NdGR tired of this, not sure it's relevant to the perf demo

    # verify optimized tree
    # TODO this uses the r3232 primitive introduced by the extension
    # not ported to here

    # Test that symbols only get parsed as functions if there's an opening
    # parenthesis.
    wrapper.command('bookmark', b'only', rev=b'9')
    assert_revset_list(repo, 'only', [9])
    # Outer "only" is a function, inner "only" is the bookmark
    assert_revset_list(repo, 'only(only)', [8, 9])

    # ':y' behaves like '0:y', but can't be rewritten as such since the
    # revision '0' may be hidden (issue5385)
    # TODO the point of this one is to check the rewriting,
    # we'll need to inspect the AST (actually it would be better to
    # separate concerns, here)
    assert_revset_list(repo, ':', list(range(10)))
    assert_revset_list(repo, ':1', [0, 1])
    assert_revset_list(repo, ':(1|2)', [0, 1, 2])
    assert_revset_list(repo, ':(1&2)', [])

    # infix/suffix resolution of ^ operator (issue2884, issue5764):

    # x^:y means (x^):y
    assert_revset_list(repo, '1^:2', [0, 1, 2])
    assert_revset_list(repo, '1^::2', [0, 1, 2])
    assert_revset_list(repo, '1^..2', [0, 1, 2])
    assert_revset_list(repo, '9^:', [8, 9])
    assert_revset_list(repo, '9^::', [8, 9])
    assert_revset_list(repo, '9^..', [8, 9])

    #  x^:y should be resolved before omitting group operators
    # TODO again a case of AST assertion
    with pytest.raises(error.ParseError):
        repo.revs('1^(:2)')

    # x^:y should be resolved recursively
    assert_revset_list(repo, 'sort(1^:2)', [0, 1, 2])
    assert_revset_list(repo, '(3^:4)^:2', [0, 1, 2])
    assert_revset_list(repo, '(3^::4)^::2', [0, 1, 2])
    assert_revset_list(repo, '(9^:)^:', [4, 5, 6, 7, 8, 9])

    # x^ in alias should also be resolved
    # NdGR these are actually testing our debug_revspec() helper!
    # They should stay at the functional layer
    # using 'AL' instead of 'A' to avoid being an ambiguous node prefix
    repo.ui.setconfig(b'revsetalias', b'AL', b'1^:2')
    assert debug_revspec(repo, 'AL') == [0, 1, 2]
    repo.ui.setconfig(b'revsetalias', b'AL', b'1^')
    assert debug_revspec(repo, 'AL:2') == [0, 1, 2]

    # but not beyond the boundary of alias expansion, because the resolution
    # should  be made at the parsing stage
    repo.ui.setconfig(b'revsetalias', b'AL', b':2')
    # TODO again AST analysis
    with pytest.raises(error.ParseError):
        debug_revspec(repo, '1^AL')

    # :: itself isn't a valid expression
    with pytest.raises(error.ParseError):
        repo.revs('::')

    # ancestor can accept 0 or more arguments
    assert_revset_list(repo, 'ancestor()', [])
    assert_revset_list(repo, 'ancestor(1)', [1])
    assert_revset_list(repo, 'ancestor(4, 5)', [1])
    assert_revset_list(repo, 'ancestor(4, 5) and 4', [])
    assert_revset_list(repo, 'ancestor(0, 0, 1, 3)', [0])
    assert_revset_list(repo, 'ancestor(3, 1, 5, 3, 5, 1)', [1])
    assert_revset_list(repo, 'ancestor(0, 1, 3, 5)', [0])
    assert_revset_list(repo, 'ancestor(1, 2, 3, 5)', [1])

    # test ancestors
    # TODO print of graphlog as courtesy for people investigating errors
    assert_revset_list(repo, 'ancestors(5)', [0, 1, 3, 5])
    assert_revset_list(repo, 'ancestor(ancestors(5))', [0])
    # TODO port r3232
    # assert_revset_list(repo, '::r3232', [0, 1, 2, 3])

    # test common ancestors
    assert_revset_list(repo, 'commonancestors(7 + 9)', [0, 1, 2, 4])
    assert_revset_list(repo, 'commonancestors(heads(all()))', [0, 1, 2, 4])
    assert_revset_list(repo, 'commonancestors(9)', [0, 1, 2, 4, 8, 9])
    assert_revset_list(repo, 'commonancestors(8 + 9)', [0, 1, 2, 4, 8])

    # test the specialized implementation of heads(commonancestors(..))
    # (2 gcas is tested in test-merge-criss-cross.t)
    assert_revset_list(repo, 'heads(commonancestors(7 + 9))', [4])
    assert_revset_list(repo, 'heads(commonancestors(heads(all())))', [4])
    assert_revset_list(repo, 'heads(commonancestors(9))', [9])
    assert_revset_list(repo, 'heads(commonancestors(8 + 9))', [8])

    # test ancestor variants of empty revision
    assert_revset_list(repo, 'ancestor(none())', [])
    assert_revset_list(repo, 'ancestors(none())', [])
    assert_revset_list(repo, 'commonancestors(none())', [])
    assert_revset_list(repo, 'heads(commonancestors(none()))', [])

    # test ancestors with depth limit

    # (depth=0 selects the node itself)
    assert_revset_list(repo, 'reverse(ancestors(9, depth=0))', [9])
    # (interleaved: '4' would be missing if heap queue were higher depth first)
    assert_revset_list(repo, 'reverse(ancestors(8:9, depth=1))', [9, 8, 4])
    # (interleaved: '2' would be missing if heap queue were higher depth first)
    assert_revset_list(repo, 'reverse(ancestors(7+8, depth=2))',
                       [8, 7, 6, 5, 4, 2])
    # (walk example above by separate queries)
    assert_revset_list(
        repo,
        'reverse(ancestors(8, depth=2)) + reverse(ancestors(7, depth=2))',
        [8, 4, 2, 7, 6, 5])
    # (walk 2nd and 3rd ancestors)
    assert_revset_list(repo, 'reverse(ancestors(7, depth=3, startdepth=2))',
                       [5, 4, 3, 2])
    # (interleaved: '4' would be missing if higher-depth ancestors
    # weren't scanned)
    assert_revset_list(repo, 'reverse(ancestors(7+8, depth=2, startdepth=2))',
                       [5, 4, 2])
    # (note that 'ancestors(x, depth=y, startdepth=z)' does not identical to
    # 'ancestors(x, depth=y) - ancestors(x, depth=z-1)'
    # because a node may have  multiple depths)
    assert_revset_list(
        repo,
        'reverse(ancestors(7+8, depth=2) - ancestors(7+8, depth=1))',
        [5, 2])

    # test bad arguments passed to ancestors()
    with pytest.raises(error.ParseError):
        repo.revs(b'ancestors(., depth=-1)')
    with pytest.raises(error.ParseError):
        repo.revs(b'ancestors(., depth=foo)')

    # test descendants
    # TODO print of graphlog as courtesy for people investigating errors

    # (null is ultimate root and has optimized path)
    assert_revset_list(repo, 'null:4 & descendants(null)', [-1, 0, 1, 2, 3, 4])
    #  (including merge)
    assert_revset_list(repo, ':8 & descendants(2+5)', [2, 4, 5, 6, 7, 8])

    # test descendants with depth limit

    # (depth=0 selects the node itself)
    assert_revset_list(repo, 'descendants(0, depth=0)', [0])
    assert_revset_list(repo, 'null: & descendants(null, depth=0)', [-1])
    # (p2 = null should be ignored)
    assert_revset_list(repo, 'null: & descendants(null, depth=2)', [-1, 0, 1])
    # (multiple paths: depth(6) = (2, 3))
    assert_revset_list(repo, 'descendants(1+3, depth=2)', [1, 2, 3, 4, 5, 6])
    # (multiple paths: depth(5) = (1, 2), depth(6) = (2, 3))
    assert_revset_list(repo, 'descendants(3+1, depth=2, startdepth=2)',
                       [4, 5, 6])
    # (multiple depths: depth(6) = (0, 2, 4), search for depth=2)
    assert_revset_list(repo, 'descendants(0+3+6, depth=3, startdepth=1)',
                       [1, 2, 3, 4, 5, 6, 7])
    # (multiple depths: depth(6) = (0, 4), no match)
    assert_revset_list(repo, 'descendants(0+6, depth=3, startdepth=1)',
                       [1, 2, 3, 4, 5, 7])

    # test ancestors/descendants relation:
    assert_revset_list(repo, 'tip#generations', [0, 1, 2, 4, 8, 9])
    assert_revset_list(repo, '3#g', [0, 1, 3, 5, 6, 7])
    # TODO maybe assert on the AST for that one
    assert_revset_list(repo, 'tip#g', [0, 1, 2, 4, 8, 9])

    # test ancestors/descendants relation subscript:
    assert_revset_list(repo, 'tip#generations[0]', [9])
    assert_revset_list(repo, '.#generations[-1]', [8])
    assert_revset_list(repo, '.#g[(-1)]', [8])
    assert_revset_list(repo, '6#generations[0:1]', [6, 7])
    assert_revset_list(repo, '6#generations[-1:1]', [4, 5, 6, 7])
    assert_revset_list(repo, '6#generations[0:]', [6, 7])
    assert_revset_list(repo, '5#generations[:0]', [0, 1, 3, 5])
    assert_revset_list(repo, '3#generations[:]', [0, 1, 3, 5, 6, 7])
    assert_revset_list(repo, 'tip#generations[1:-1]', [])

    # NdGR that one with AST (debugrevspec)
    assert_revset_list(repo, 'roots(:)#g[2]', [2, 3])

    # test author
    assert_revset_list(repo, 'author(bob)', [2])
    assert_revset_list(repo, 'author("re:bob|test")', list(range(10)))
    assert_revset_list(repo, r'author(r"re:\S")', list(range(10)))
    assert_revset_list(repo, 'branch(é)', [8, 9])
    assert_revset_list(repo, 'branch(a)', [0])
    assert [(r, repo[r].branch())
            for r in repo.revs('branch("re:a")')
            ] == [(0, b'a'),
                  (2, b'a-b-c-'),
                  (3, b'+a+b+c+'),
                  (4, b'-a-b-c-'),
                  (5, b'!a/b/c/'),
                  (6, b'_a_b_c_'),
                  (7, b'.a.b.c.'),
                  ]
    assert_revset_list(repo, 'children(4)', [6, 8])
    assert_revset_list(repo, 'children(null)', [0])
    assert_revset_list(repo, 'closed()', [])

    # TODO too hacky, should be enclosed
    repo.dirstate._cwd = repo.root
    assert_revset_list(repo, b'contains(a)', [0, 1, 3, 5])

    # NdGR had to change because B can match a sha (does not happen with
    # the tricks the .t system does)
    assert_revset_list(repo, 'desc(Bu)', [5])

    assert [(r, repo[r].description().splitlines()[0])
            for r in repo.revs('desc(r"re:S?u")')
            ] == [(5, b'5 bug'),
                  (6, b'6 issue619'),
                  ]

    assert_revset_list(repo, 'descendants(2 or 3)', list(range(2, 10)))
    assert_revset_list(repo, 'file("b*")', [1, 4])
    assert_revset_list(repo, 'filelog(b)', [1, 4])
    assert_revset_list(repo, 'filelog("../repo/b")', [1, 4])
    assert_revset_list(repo, 'follow()', [0, 1, 2, 4, 8, 9])
    assert_revset_list(repo, r'grep("issue\d+")', [6])

    # invalid regular expression
    with pytest.raises(error.ParseError):
        repo.revs(b'grep("(")')

    assert_revset_list(repo, r'grep("\bissue\d+")', [])
    with pytest.raises(error.ParseError):
        repo.revs(br'grep(r"\")')

    assert_revset_list(repo, 'head()', [0, 1, 2, 3, 4, 5, 6, 7, 9])

    # Test heads
    assert_revset_list(repo, 'heads(6::)', [7])

    # heads() can be computed in subset '9:'
    assert_revset_list(repo, '9: & heads(all())', [9])

    # but should follow the order of the subset
    assert_revset_list(repo, 'heads(all())', [7, 9])
    assert_revset_list(repo, 'heads(tip:0)', [7, 9])
    assert_revset_list(repo, 'tip:0 & heads(0:tip)', [9, 7])

    assert_revset_list(repo, 'keyword(issue)', [6])
    assert_revset_list(repo, 'keyword("test a")', [])

    # Test first (=limit) and last
    assert_revset_list(repo, 'limit(head(), 1)', [0])
    assert_revset_list(repo, 'limit(author("re:bob|test"), 3, 5)', [5, 6, 7])
    assert_revset_list(repo, 'limit(author("re:bob|test"), offset=6)', [6])
    assert_revset_list(repo, 'limit(author("re:bob|test"), offset=10)', [])

    with pytest.raises(error.ParseError):
        repo.revs(b'limit(all(), 1, -1)')
    with pytest.raises(error.ParseError):
        repo.revs(b'limit(all(), -1)')
    assert_revset_list(repo, 'limit(all(), 0)', [])
    with pytest.raises(error.ParseError):
        repo.revs(b'last(all(), -1)')
    assert_revset_list(repo, 'last(all(), 0)', [])
    assert_revset_list(repo, 'last(all(), 1)', [9])
    assert_revset_list(repo, 'last(all(), 2)', [8, 9])
