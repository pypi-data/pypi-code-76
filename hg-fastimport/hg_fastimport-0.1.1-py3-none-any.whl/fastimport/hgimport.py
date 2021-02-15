# Copyright (C) 2008 Canonical Ltd
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

"""Processor of import commands.

This module provides core processing functionality including an abstract class
for basing real processors on. See the processors package for examples.
"""

import os
import shutil
import stat
import sys

from contextlib import closing

from hgext.convert import common, hg as converthg
from mercurial import util, zstd
from mercurial.i18n import _

from .vendor.python_fastimport import processor, parser

# When dealing with many blobs, a database is more efficient
# than a filesystem. However, it's not necessary for us to work.
try:
    import sqlite3
    have_sqlite = True
except (ImportError):
    have_sqlite = False


class fastimport_source(common.converter_source):
    """Interface between the fastimport processor below and Mercurial's
    normal conversion infrastructure.
    """
    def __init__(self, ui, repotype, repo, sources, blobpath):
        self.ui = ui
        self.sources = sources
        self.processor = HgImportProcessor(ui, repo, blobpath)
        self.parsed = False
        self.repotype = repotype

    # converter_source methods

    def before(self):
        self.processor.setup()

    def after(self):
        self.processor.teardown()

    def getheads(self):
        """Return a list of this repository's heads"""
        self._parse()
        allheads = []
        for branchheads in self.processor.branchmap.values():
            allheads.extend(branchheads)
        return allheads

    def getfile(self, name, fileid):
        if fileid is None:              # deleted file
            return None, None
        return (self.processor.getblob(fileid),
                self.processor.getmode(name, fileid))

    def getchanges(self, commitid, full):
        """Returns a tuple of (files, copies, cleanp2).

        files is a sorted list of (filename, id) tuples for all files
        changed between commitid and its first parent returned by
        getcommit().
        commitid id is the source revision id of the file.
        cleanp2 is currently unused and an empty set is returned.

        copies is a dictionary of dest: source
        """
        if full:
            raise util.Abort(_("convert from fastimport does not support --full"))
        return (self.processor.modified[commitid],
                self.processor.copies[commitid],
                set())

    def getcommit(self, commitid):
        """Return the commit object for commitid"""
        if commitid is None:
            return None
        else:
            return self.processor.commitmap[commitid]

    def gettags(self):
        """Return the tags as a dictionary of name: revision"""
        # oops, this loses order
        return dict(self.processor.tags)

    def getchangedfiles(self, rev, i):
        """Return the files changed by rev compared to parent[i].

        i is an index selecting one of the parents of rev.  The return
        value should be the list of files that are different in rev and
        this parent.

        If rev has no parents, i is None.

        This function is only needed to support --filemap
        """
        raise NotImplementedError()

    # private worker methods

    def _parse(self):
        if self.parsed:
            return
        for source in self.sources:
            if source == b"-":
                infile = sys.stdin
            else:
                infile = open(source, 'rb')
            try:
                p = parser.ImportParser(infile)
                self.processor.process(p.iter_commands)
            finally:
                if infile is not sys.stdin:
                    infile.close()
        self.parsed = True


class HgImportProcessor(processor.ImportProcessor):

    tagprefix = b"refs/tags/"

    def __init__(self, ui, repo, blobpath):
        super(HgImportProcessor, self).__init__()
        self.ui = ui
        self.repo = repo

        self.commitmap = {}             # map commit ID (":1") to commit object
        self.branchmap = {}             # map branch name to list of heads

        # see HgImportCommitHandler for details on these three
        self.modified = {}              # map commit id to list of file mods
        self.filemodes = {}             # map commit id to {filename: mode} map
        self.copies = {}                # map commit id to dict of file copies

        self.tags = []                  # list of (tag, mark) tuples

        self.numblobs = 0               # for progress reporting
        if blobpath:
            self.blobpath = blobpath
            self.blobpersist = True
        else:
            self.blobpath = os.path.join(self.repo.root, b".hg", b"blobs")
            self.blobpersist = False
        self.blobdb = None
        self.compressor = zstd.ZstdCompressor(level = 6) # compress the blob
        self.decompressor = zstd.ZstdDecompressor()      # decompress the blob

    def setup(self):
        """Setup before processing any streams."""
        pass

    def teardown(self):
        """Cleanup after processing all streams."""
        if self.blobdb:
            self.blobdb.commit()
            self.blobdb.close()
            self.blobdb = None
            if self.blobpersist:
                self.ui.debug(b"Persisting blob database %s ...\n"
                              % self.blobpath)
            else:
                self.ui.debug(b"Removing blob database %s ...\n"
                              % self.blobpath)
                os.remove(self.blobpath)
        elif os.path.exists(self.blobpath):
            if self.blobpersist:
                self.ui.debug(b"Persisting blob directory %s ...\n"
                              % self.blobpath)
            else:
                self.ui.debug(b"Removing blob directory %s ...\n"
                          % self.blobpath)
                shutil.rmtree(self.blobpath)

    def progress_handler(self, cmd):
        self.ui.write(b"Progress: %s\n" % cmd.message)

    def blob_handler(self, cmd):
        self.writeblob(cmd.id, cmd.data)

    def _openblobdb(self):
        self.blobdb = sqlite3.connect(self.blobpath)
        self.blobdb.text_factory = str
        self.blobdb.execute("CREATE TABLE IF NOT EXISTS blob(id varchar PRIMARY KEY NOT NULL, content blob NOT NULL)")

    def _getblobfilename(self, blobid):
        # XXX should escape ":" for windows
        return os.path.join(self.blobpath, b"blob-" + blobid)

    def writeblob(self, blobid, data):
        data = self.compressor.compress(data)

        if have_sqlite:
            if self.blobdb is None:
                self._openblobdb()
            self.blobdb.execute("INSERT OR IGNORE INTO blob(id, content) VALUES(?, ?)",
                                (blobid, data))
        else:
            fn = self._getblobfilename(blobid)
            if not os.path.isfile(fn):
                if not os.path.exists(self.blobpath):
                    os.mkdir(self.blobpath)
                with open(fn, "wb") as f:
                    f.write(data)

        self.numblobs += 1
        if self.numblobs % 500 == 0:
            self.ui.status(b"%d blobs read\n" % self.numblobs)

    def getblob(self, fileid):
        (commitid, blobid) = fileid

        if have_sqlite:
            if self.blobdb is None:
                self._openblobdb()
            with closing(self.blobdb.cursor()) as c:
                c.execute("SELECT content FROM blob WHERE id=?", (blobid,))
                data, = c.fetchone()
        else:
            fn = self._getblobfilename(blobid)
            if os.path.isfile(fn):
                with open(fn, "rb") as f:
                    data = f.read()

        if not data:
            raise RuntimeError("missing blob %s for fileid %s"
                               % (blobid, fileid))
        return self.decompressor.decompress(data, 10**8)

    def getmode(self, name, fileid):
        (commitid, blobid) = fileid
        return self.filemodes[commitid][name]

    def checkpoint_handler(self, cmd):
        # This command means nothing to us
        pass

    def _getcommit(self, commitref):
        """Given a mark reference or a branch name, return the
        appropriate commit object.  Return None if commitref is a tag
        or a branch with no commits.  Raises KeyError if anything else
        is out of whack.
        """
        if commitref.startswith(b":"):
            # KeyError here indicates the input stream is broken.
            return self.commitmap[commitref]
        elif commitref.startswith(self.tagprefix):
            return None
        else:
            branch = self._getbranch(commitref)
            if branch is None:
                raise ValueError(b"invalid commit ref: %s" % commitref)

            heads = self.branchmap.get(branch)
            if heads is None:
                return None
            else:
                # KeyError here indicates bad commit id in self.branchmap.
                return self.commitmap[heads[-1]]

    def _getbranch(self, ref):
        """Translate a Git head ref to corresponding Mercurial branch
        name.  E.g. \"refs/heads/foo\" is translated to \"foo\".
        Special case: \"refs/heads/master\" becomes \"default\".  If
        'ref' is not a head ref, return None.
        """
        prefix = b"refs/heads/"
        if ref.startswith(prefix):
            branch = ref[len(prefix):]
            if branch == b"master":
                return b"default"
            else:
                return branch
        else:
            return None

    def commit_handler(self, cmd):
        # XXX this assumes the fixup branch name used by cvs2git.  In
        # contrast, git-fast-import(1) recommends "TAG_FIXUP" (not under
        # refs/heads), and implies that it can be called whatever the
        # creator of the fastimport dump wants to call it.  So the name
        # of the fixup branch should be configurable!
        fixup = (cmd.ref == b"refs/heads/TAG.FIXUP")

        if cmd.ref.startswith(self.tagprefix) and cmd.mark:
            tag = cmd.ref[len(self.tagprefix):]
            self.tags.append((tag, b':' + cmd.mark))

        if cmd.from_:
            first_parent = cmd.from_
        else:
            first_parent = self._getcommit(cmd.ref) # commit object
            if first_parent is not None:
                first_parent = first_parent.rev     # commit id

        if cmd.merges:
            if len(cmd.merges) > 1:
                raise NotImplementedError("Can't handle more than two parents")
            second_parent = cmd.merges[0]
        else:
            second_parent = None

        if first_parent is None and second_parent is not None:
            # First commit on a new branch that has 'merge' but no 'from':
            # special case meaning branch starts with no files; the contents of
            # the first commit (this one) determine the list of files at branch
            # time.
            first_parent = second_parent
            second_parent = None
            no_files = True             # XXX this is ignored...

        bfirst_parent = first_parent or b''
        bsecond_parent = second_parent or b''
        self.ui.debug(b"commit %s: first_parent = %s, second_parent = %s\n"
                      % (cmd, bfirst_parent, bsecond_parent))
        assert ((first_parent != second_parent) or
                (first_parent is second_parent is None)), \
               (b"commit %s: first_parent == second parent = %s"
                % (cmd, bfirst_parent))

        # Figure out the Mercurial branch name.
        if fixup and first_parent is not None:
            # If this is a fixup commit, pretend it happened on the same
            # branch as its first parent.  (We don't want a Mercurial
            # named branch called "TAG.FIXUP" in the output repository.)
            branch = self.commitmap[first_parent].branch
        else:
            branch = self._getbranch(cmd.ref)

        commit_handler = HgImportCommitHandler(
            self, cmd, self.ui)
        commit_handler.process()
        self.modified[cmd.id] = commit_handler.modified
        self.filemodes[cmd.id] = commit_handler.mode
        self.copies[cmd.id] = commit_handler.copies

        # in case we are converting from git or bzr, prefer author but
        # fallback to committer (committer is required, author is
        # optional)
        userinfo = cmd.author or cmd.committer
        if userinfo[0] == userinfo[1]:
            # In order to conform to fastimport syntax, cvs2git with no
            # authormap produces author names like "jsmith <jsmith>"; if
            # we see that, revert to plain old "jsmith".
            user = userinfo[0]
        else:
            user = b"%s <%s>" % (userinfo[0], userinfo[1])

        text = cmd.message
        date = self.convert_date(userinfo)
        parents = []
        if first_parent:
            parents.append(first_parent)
        if second_parent:
            parents.append(second_parent)

        commit = common.commit(user, date, text, parents, branch,
                               rev=cmd.id, sortkey=int(cmd.id[1:]))

        self.commitmap[cmd.id] = commit
        heads = self.branchmap.get(branch)
        if heads is None:
            heads = [cmd.id]
        else:
            # adding to an existing branch: replace the previous head
            try:
                heads.remove(first_parent)
            except ValueError:          # first parent not a head: no problem
                pass
            heads.append(cmd.id)        # at end means this is tipmost
        self.branchmap[branch] = heads
        self.ui.debug(b"processed commit %s\n" % cmd)

    def convert_date(self, c):
        res = (int(c[2]), -int(c[3]))
        #print c, res
        #print type((0, 0)), type(res), len(res), type(res) is type((0, 0))
        #if type(res) is type((0, 0)) and len(res) == 2:
        #    print "go for it"
        #return res
        return b"%d %d" % res

    def reset_handler(self, cmd):
        branch = self._getbranch(cmd.ref)
        if branch:
            # The usual case for 'reset': (re)create the named branch.
            # XXX what should we do if cmd.from_ is None?
            if cmd.from_ is not None:
                self.branchmap[branch] = [cmd.from_]
            else:
                # pretend the branch never existed... is this right?!?
                try:
                    del self.branchmap[branch]
                except KeyError:
                    pass
            #else:
            #    # XXX filename? line number?
            #    self.ui.warn("ignoring branch reset with no 'from'\n")
        elif cmd.ref.startswith(self.tagprefix):
            # Create a "lightweight tag" in Git terms.  As I understand
            # it, that's a tag with no description and no history --
            # rather like CVS tags.  cvs2git turns CVS tags into Git
            # lightweight tags, so we should make sure they become
            # Mercurial tags.  But we don't have to fake a history for
            # them; save them up for the end.
            if cmd.from_ is not None:
                tag = cmd.ref[len(self.tagprefix):]
                self.tags.append((tag, cmd.from_))

    def tag_handler(self, cmd):
        pass


class HgImportCommitHandler(processor.CommitHandler):

    def __init__(self, parent, command, ui):
        self.parent = parent            # HgImportProcessor running the show
        self.command = command          # CommitCommand that we're processing
        self.ui = ui

        # Files changes by this commit as a list of (filename, id)
        # tuples where id is (commitid, blobid).  The blobid is
        # needed to fetch the file's contents later, and the commitid
        # is needed to fetch the mode.
        # (XXX what about inline file contents?)
        # (XXX how to describe deleted files?)
        self.modified = []

        # mode of files listed in self.modified: '', 'x', or 'l'
        self.mode = {}

        # dictionary of src: dest (renamed files are in here and self.modified)
        self.copies = {}

        # number of inline files seen in this commit
        self.inlinecount = 0

    def copy_handler(self, filecmd):
        self.copies[filecmd.src_path] = filecmd.dest_path

    def delete_handler(self, filecmd):
        self.modified.append((filecmd.path, None))

    def deleteall_handler(self, filecmd):
        pass # Fossil fastexport will hit this with no parents

    def modify_handler(self, filecmd):
        if filecmd.dataref:
            blobid = filecmd.dataref    # blobid is the mark of the blob
        else:
            blobid = b"%s-inline:%d" % (self.command.id, self.inlinecount)
            assert filecmd.data is not None
            self.parent.writeblob(blobid, filecmd.data)
            self.inlinecount += 1

        fileid = (self.command.id, blobid)

        self.modified.append((filecmd.path, fileid))
        if stat.S_ISLNK(filecmd.mode): # link
            mode = b'l'
        elif filecmd.mode & 0o111: # executable
            mode = b'x'
        elif stat.S_ISREG(filecmd.mode): # regular file
            mode = b''
        else:
            raise RuntimeError(b"mode %s unsupported" % filecmd.mode)

        self.mode[filecmd.path] = mode

    def rename_handler(self, filecmd):
        # copy oldname to newname and delete oldname
        self.copies[filecmd.new_path] = filecmd.old_path
        self.modified.append((filecmd.old_path, None))
