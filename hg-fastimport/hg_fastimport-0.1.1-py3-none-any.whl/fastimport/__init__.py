""" import Git fast-import streams """
from __future__ import absolute_import

from mercurial import (
    commands,
    encoding,
    error,
    pycompat,
)

from mercurial.i18n import _

from hgext.convert import (
    convcmd,
    hg,
)

from .hgimport import fastimport_source

__version__ = b"0.1.1"
testedwith = b"5.6.1"
minimumhgversion = b"4.1"

cmdtable = {}
try:
    from mercurial import registrar
    command = registrar.command(cmdtable)
except (ImportError, AttributeError):
    from mercurial import cmdutil
    command = cmdutil.command(cmdtable)

@command(b"fastimport",
         [(b"", b"branchsort", None, _(b"try to sort changesets by branches")),
          (b"", b"datesort", None, _(b"try to sort changesets by date")),
          (b"", b"sourcesort", None, _(b"preserve source changesets order")),
          (b"", b"blobpath", b"", _(b"path for persistent blob data"))],
         _(b"hg fastimport SOURCE ..."),
          norepo=False)

def fastimport(ui, repo, *sources, **opts):
    """Convert a git fastimport dump into Mercurial changesets.

    Reads a series of SOURCE fastimport dumps and adds the resulting
    changes to the current Mercurial repository.
    """
    # Would be nice to just call hgext.convert.convcmd.convert() and let
    # it take care of things.  But syntax and semantics are just a
    # little mismatched:
    #   - fastimport takes multiple source paths (mainly because cvs2git
    #     produces 2 dump files)
    #   - fastimport's dest is implicitly the current repo
    #
    # So for the time being, I have copied bits of convert() over here.
    # Boo, hiss.

    if not sources:
        sources = (b"-")

    opts = pycompat.byteskwargs(opts)

    # assume fastimport metadata (usernames, commit messages) are
    # encoded UTF-8
    convcmd.orig_encoding = encoding.encoding
    encoding.encoding = b"UTF-8"

    # sink is the current repo, src is the list of fastimport streams
    destc = hg.mercurial_sink(ui, b"hg", repo.root)
    srcc = fastimport_source(ui, b"fastimport", repo, sources,
                             opts[b"blobpath"])

    defaultsort = b"branchsort"          # for efficiency and consistency
    sortmodes = (b"branchsort", b"datesort", b"sourcesort")
    sortmode = [m for m in sortmodes if opts.get(m)]
    if len(sortmode) > 1:
        raise error.Abort(_(b"more than one sort mode specified"))
    if sortmode:
        sortmode = sortmode[0]
    else:
        sortmode = defaultsort

    # not implemented: filemap, revmapfile
    revmapfile = destc.revmapfile()
    c = convcmd.converter(ui, srcc, destc, revmapfile, opts)
    c.convert(sortmode)
