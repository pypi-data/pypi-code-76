"This module contains abtractions for managed repositories."
import os
import os.path as osp
import urllib.parse
import tarfile
import zipfile
from subprocess import check_output as call

from mercurial import hg, error, commands, archival, scmutil, util
from .hgcompat import pull as hgpull, push as hgpush
from .utils import download_file, WrappedRepo


class rcbase(object):

    hex = ''
    phase = ''
    tags = ()
    revnum = -1
    branch = ''

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.hex == other.hex

    def __ne__(self, other):
        return not self == other

    @property
    def parents(self):
        return (self,)

    def ancestors(self):
        return ()

    def descendants(self):
        return ()

    def obsolete(self):
        return False


class revisioncontext(rcbase):

    def __init__(self, cset):
        self._cset = cset
        # be careful with the 'next commit'
        self._hex = cset.hex() if cset.node() is not None else None
        tags = set(cset.tags()) - set([b'tip'])
        self._tag = min(tags, key=len) if tags else None
        self._branch = cset.branch()

    @property
    def hex(self):
        return self._hex and self._hex.decode('utf-8') or None

    @property
    def tag(self):
        return self._tag and self._tag.decode('utf-8') or None

    @property
    def branch(self):
        return self._branch and self._branch.decode('utf-8') or None

    @property
    def parents(self):
        return [revisioncontext(p)
                for p in self._cset.parents()]

    @property
    def phase(self):
        return self._cset.phasestr().decode('utf-8')

    @property
    def tags(self):
        return [
            t.decode('utf-8')
            for t in self._cset.tags()
        ]

    @property
    def revnum(self):
        return self._cset.rev()

    def ancestors(self):
        return (revisioncontext(cset)
                for cset in self._cset.ancestors())

    def descendants(self):
        return (revisioncontext(cset)
                for cset in self._cset.descendants())

    def obsolete(self):
        return self._cset.obsolete()


class gitrevisioncontext(rcbase):

    def _call(self, *args):
        return call(
            ('git',) + args, cwd=self.path
        ).strip().decode('utf-8')

    def __init__(self, path, hex=None):
        self.path = path
        if hex is None:
            # No explicit rev: Find the long hash of the current one.
            args = ['show', '--no-patch', '--format=format:%H']
            try:
                out = self._call(*args)
                self.hex = out
            except Exception:
                self.hex = None

        # Get tag / dist information about the specified rev.
        # When there are tags, "git describe" outputs a string separated by
        # dashes, hence the "split" call.
        # Use --abbrev=40 in "git describe" commands to always work with long
        # git revs (same as we do with hg revs). This is also coherent with the
        # "git rev-parse" call below, which gets a long rev.
        if self.hex:
            args = ['describe', '--long', '--tags', '--always', '--abbrev=40',
                    self.hex]
            try:
                out = self._call(*args)
                tag, dist, _hex = (['', ''] + out.rsplit('-', 2))[-3:]
                self.tag = tag if dist == '0' else None
            except Exception:
                self.tag = None
        else:
            self.tag = None

        # Get the name of the current branch.
        branch = self._call('rev-parse', '--abbrev-ref', 'HEAD')
        self.branch = branch

    @property
    def tags(self):
        if self.tag:
            return [self.tag]
        return []

    @property
    def revnum(self):
        return None

    @property
    def parents(self):
        return [self]

    @property
    def phase(self):
        return ''

    def ancestors(self):
        out = self._call('rev-list', self.hex)
        return out.splitlines()

    def descendants(self):
        out = self._call('rev-list', '--children', self.hex)
        return out.splitlines()


def repoclassbyconf(conf, path, hggit=False):
    '''introspect the configuration parameters values and the filesystem
    and deduct the right repository manager class.
    '''
    uri = urllib.parse.urlparse(conf['pulluri'])
    pulluri = conf['pulluri']

    # first check the local repo (if it exists)
    if (osp.isdir(osp.join(path, '.hg'))
        or osp.isdir(osp.join(pulluri, '.hg'))):
        return hgrepo

    if osp.isdir(osp.join(path, '.git')):
        return gitrepo

    # then the hg-vs-git-vs-hggit
    if (uri.scheme == 'git' or
        uri.path.endswith('.git') or
        osp.isdir(osp.join(pulluri, '.git'))):
        if hggit:
            return hgrepo
        return gitrepo

    if uri.path.endswith('.tar.gz') or uri.path.endswith('.tar.bz2'):
        return tgzrepo

    if uri.path.endswith('.zip'):
        return ziprepo
    return hgrepo


class managedrepo(object):
    """Abstracts a repository and its essential operations.
    This object dispatches to the actual class (for hg or git)

    Class methods:

    - clone(ui, source, dest, conf): clone the managed repository at
      `source` to `dest`.

    Instance properties:

    - conf: configuration entries of the managed repository
    - ui: mercurial.ui.ui instance
    - root: root path of the managed repository

    Instance methods:

    - update_or_pull_and_update(section, secconf, rev): update the
      repository up to the given revision `rev`.

    - isshared(): True if the repository is shared

    - currentctx(): a `revisioncontext` instance representing of parent context

    - workingctx(): a `revisioncontext` instance representing the working context

    - revsingle(rev): a `revisioncontext` instance representing the
      context of the given revision `rev`

    - check_dirty(): True if the working context is not clean

    - changestatus(): a string given details about modification on the working context

    - unknown_rev(rev): True if the given revision `rev` is not known by the repository

    """

    def __init__(self, conf, path):
        self.conf = conf
        self.ui = conf.ui

class tgzrepo(managedrepo):
    """ A tarball repository """
    __slots__ = ('conf', 'ui', 'root')

    @classmethod
    def clone(cls, ui, source, dest, conf):
        with download_file(source) as fp:
            tf = tarfile.open(fileobj=fp, mode='r:*')
            if not os.path.exists(dest):
                os.makedirs(dest)
            # most of the time, the final folder is archivec
            # we would like it to be the final dest
            if set(m.name.split('/', 1)[0] for m in tf.members) == {os.path.basename(dest)}:
                dest = os.path.dirname(dest) or '.'
            tf.extractall(dest)

    def __init__(self, conf, path):
        super(tgzrepo, self).__init__(conf, path)
        self.root = path

    def isshared(self):
        return False

    def currentctx(self, allow_p2=False):
        return rcbase()

    def workingctx(self):
        return rcbase()

    def check_dirty(self, section):
        return rcbase()

    def revsingle(self, rev, skiperror=False):
        return rcbase()

    def unknown_rev(self, rev):
        return False

    def changestatus(self):
        return ''

    def update_or_pull_and_update(self, section, secconf, rev):
        pass

    def pull_repo(self, section, conf):
        pass


class ziprepo(tgzrepo):
    """ A zip repository """
    __slots__ = ('conf', 'ui', 'root')

    @classmethod
    def clone(cls, ui, source, dest, conf):
        with download_file(source) as fp:
            tf = zipfile.ZipFile(fp, mode='r')
            if not os.path.exists(dest):
                os.makedirs(dest)
            tf.extractall(dest)


class gitrepo(managedrepo):
    """ A git repository """
    __slots__ = ('conf', 'ui', 'root')

    @classmethod
    def clone(cls, ui, source, dest, conf):
        call(['git', 'clone', source, dest])

    def __init__(self, conf, path):
        super(gitrepo, self).__init__(conf, path)
        self.root = path
        self.revcontext = gitrevisioncontext(self.root)

    def _call(self, *args):
        try:
            return call(
                ('git',) + args, cwd=self.root
            ).strip().decode('utf-8')
        except Exception as exc:
            # stdout will show the shit
            pass

    def isshared(self):
        return False

    def currentctx(self, allow_p2=False):
        return self.revcontext

    def workingctx(self):
        return self.revcontext

    def check_dirty(self, section):
        changes = self.changestatus()
        if changes:
            self.ui.write('%s repo is unclean, please adjust\n' % section,
                          label='confman.dirty')
        return changes

    def revsingle(self, rev, skiperror=False):
        try:
            out = self._call('rev-parse', rev)
            return gitrevisioncontext(self.root, hex=out)
        except:
            if skiperror:
                return None
            raise

    def unknown_rev(self, rev):
        rctx = self.revsingle(rev, skiperror=True)
        if rctx is not None:
            return False
        return True

    def changestatus(self):
        out = self._call('status', '--porcelain')
        stat = ''.join(
            sorted(set(
                [l.strip().split()[0].replace('??', 'M')
                 for l in out.splitlines()]
            ))
        )
        return stat

    def update_or_pull_and_update(self, section, secconf, rev):
        remotename = self.conf.opts.get('use_hgrc_path') or 'origin'
        self._call('fetch', remotename)
        self._call('checkout', '-q', rev)
        return not self.unknown_rev(rev)


class hgrepo(managedrepo):
    """ A mercurial repository """
    __slots__ = ('conf', 'ui', 'repo')

    def __init__(self, conf, path):
        super(hgrepo, self).__init__(conf, path)
        self.repo = WrappedRepo(
            hg.repository(self.ui, path=path.encode('utf-8'))
        )

    @property
    def root(self):
        "Root path of the repository"
        return self.repo.root

    def revsingle(self, revexpr, skiperror=False):
        """Return the highest cset of the revset matching the given revision
        expression """
        try:
            cset = scmutil.revsingle(self.repo, revexpr.encode('utf-8'))
        except:
            if skiperror:
                return None
            raise
        return revisioncontext(cset)

    def changestatus(self):
        """Check `modified, added, removed, deleted`
        ignore `unknown, ignored, clean` """
        return ''.join(tag
                       for tag, state in zip('MARD', self.repo.status())
                       if state)

    def isshared(self):
        """Check if the repository is a shared"""
        return self.repo.sharedpath != self.repo.path

    def currentctx(self, allow_p2=False):
        """Return the current context (``self[None]``).

        If ``allow_p2`` is False (default) and the current context has
        2 parents (a.k.a. merge in progress) the process is aborted.
        """
        cset = self.repo[None] # grab the current context
        if len(cset.parents()) > 1:
            self.ui.write('has two parents (uncommitted merge)\n',
                          label='confman.dirty')
            if not allow_p2:
                raise error.Abort(b'bailing out')
        return revisioncontext(cset)

    def is_on_descendant(self, rev):
        '''return True if the repository is on a descendant of ``rev``'''
        return bool(scmutil.revrange(self.repo, [b'%s::.' % rev.encode('utf-8')]))

    def workingctx(self):
        """Return the working/current context context of a repository
        Will abort if there is more than one parent (it may mean an
        ongoing merge for instance) """
        return self.currentctx().parents[0]

    @classmethod
    def clone(cls, conf, source, dest, secconf):
        """clone the `source` uri into `dest`
        The value of source can vary depening on some options:
        * share-path
        * uri-map-file
        """
        sharepath = conf.opts.get('share_path')
        if not sharepath:
            newsource = conf.rewriteuri(source)
            if newsource != source:
                conf.ui.warn('clone: using %r instead of %r\n' % (newsource, source))
                source = newsource
            return commands.clone(
                conf.ui,
                source=source.encode('utf-8'),
                dest=dest.encode('utf-8')
            )
        target = osp.join(sharepath, secconf['layout'])
        if not osp.exists(target):
            os.makedirs(target)
            commands.clone(
                conf.ui,
                source=source.encode('utf-8'),
                dest=target.encode('utf-8')
            )
        return hg.share(
            conf.ui,
            target.encode('utf-8'),
            dest.encode('utf-8')
        )

    def pull_repo(self, section, conf):
        """Pull a managed repo from its configuration
        First the default path will be used, then the `pulluri`
        is used as a fallback
        """
        ui = self.ui
        pathname = self.conf.opts.get('use_hgrc_path') or 'default'
        pathuri = self.repo.ui.expandpath(pathname.encode('utf-8'))
        if pathuri == pathname.encode('utf-8'):
            pathuri = conf['pulluri'].encode('utf-8')
            ui.warn('%s repo has no %s path, using configuration pulluri %s instead\n' %
                    (section, pathname, pathuri.decode('utf-8')))

        source, _branches = hg.parseurl(pathuri, None)
        newsource = self.conf.rewriteuri(source)
        if newsource != source:
            ui.warn('pull: using %r instead of %r\n' % (
                newsource.decode('utf-8'),
                source.decode('utf-8'))
            )
            source = newsource

        try:
            other = hg.peer(self.repo.ui, self.conf.opts, source)
            hgpull(self.repo, other)
        except error.RepoError:
            pulluri = conf['pulluri']
            if pathuri == pulluri:
                raise # we already tried
            ui.warn('%s repo cannot be pulled from its local path, using pulluri %s\n' %
                    (section, pulluri))
            source, _branches = hg.parseurl(pulluri, None)
            other = hg.peer(self.repo.ui, self.conf.opts, source)
            hgpull(self.repo, other)

    def push_repo(self, section, conf):
        self.ui.write(section + '\n', label='confman.section')
        pathname = self.conf.opts.get('use_hgrc_path', 'default')
        pathuri = self.repo.ui.expandpath(pathname.encode('utf-8')).decode('utf-8')
        if pathuri == pathname:
            pathuri = conf['pulluri']
            self.ui.warn('%s repo has no %s path, using configuration pulluri %s instead\n' %
                         (section, pathname, pathuri))
        track = conf.get('track')
        self.ui.write('pushing %s to %s\n' % (track, pathuri))
        source, __branches = hg.parseurl(pathuri.encode('utf-8'), None)
        other = hg.peer(self.repo.ui, self.conf.opts, source)
        hgpush(self.repo, other, track.encode('utf-8'))

    def unknown_rev(self, rev):
        """Predicate to check if a revision belongs to a repository """
        try:
            self.revsingle(rev)
        except (error.RepoLookupError, error.LookupError, error.Abort):
            return True
        return False

    def update(self, rev):
        "Update the repository to `rev` "
        commands.update(self.ui, self.repo, rev=rev.encode('utf-8'))

    def update_or_pull_and_update(self, section, conf, rev):
        """Try hard to update to a specified revision
        Also output a summary of the operation as descriptive as possible
        """
        ui = self.ui
        if self.unknown_rev(rev):
            self.pull_repo(section, conf)
        if self.unknown_rev(rev):
            ui.write('cannot update to %s\n' % rev, label='confman.dirty')
            return False
        wctx = self.workingctx()
        if rev in self.repo.branchmap():
            self.pull_repo(section, conf)
        currev = wctx.tag or wctx.hex
        targetctx = self.revsingle(rev)
        targetrev = targetctx.tag or targetctx.hex
        ui.write('updating to %s\n' % rev, label='confman.public-phase')
        self.update(rev)
        ui.write('updated to %s/%s from %s/%s\n' %
                 (targetrev,
                  targetctx.branch,
                  currev,
                  wctx.branch),
                 label='confman.updated')
        return True

    def check_dirty(self, section):
        """Check and log the dirtyness of a repository """
        changes = self.repo[None].dirty(missing=True)
        if changes:
            self.ui.write('%s repo is unclean, please adjust\n' % section,
                          label='confman.dirty')
        return changes

    def archive(self, zippath, prefix, rev, **opts):
        """Add an unversioned zip archive content of configuration repositories
        at ``rev`` into ``zippath`` with internal ``prefix``"""
        ctx = scmutil.revsingle(self.repo._repo, rev.encode('utf-8'))
        if not ctx:
            raise error.Abort(b'no working directory: please specify a revision')
        matchfn = scmutil.match(ctx, [], opts)
        node = ctx.node()
        archivers = archival.archivers.copy()
        archival.archivers['zip'] = zipit
        archival.archive(
            self.repo._repo,
            zippath.encode('utf-8'),
            node,
            b'zip',
            not opts.get('no_decode'),
            matchfn,
            prefix.encode('utf-8')
        )
        archival.archivers.update(archivers)

    def rewrite_conf(self, conf):
        from difflib import unified_diff
        from collections import defaultdict
        from mercurial.config import config
        from .utils import _unflatten

        # build the nested hgrc entries ([section] key value, key value, ...)
        entries = _unflatten(conf).get('hgrc', defaultdict(dict))
        entries['paths']['default'] = conf.get('pulluri')

        # first, let's remove/prune from the entries the elements that
        # already exist as is, and separate new entries from updated entries
        hgrcpath = osp.join(self.repo.path, 'hgrc')
        updated = defaultdict(dict)
        conf = config()  # TODO: implement an str friendly config-like object
        conf.read(hgrcpath.encode('utf-8'))
        for section in conf:
            usection = section.decode('utf-8')
            entry = entries.get(usection)
            if not entry:
                continue
            for key in conf[section]:
                ukey = key.decode('utf-8')
                value = conf[section][key].decode('utf-8')
                newvalue = entry.get(ukey)
                if newvalue is not None and newvalue != value:
                    updated[usection][ukey] = newvalue
                entry.pop(ukey, None)
            if not entries[usection]: # now empty
                entries.pop(usection)
        # at this point entries contains exclusively *new* entries

        # rewrite without altering otherwise fine parts of the file
        if not osp.exists(hgrcpath):
            with open(hgrcpath, 'w'):
                self.ui.write('creating an hgrc file from scratch\n')

        newhgrcpath = os.path.join(self.repo.path, 'hgrc.new')
        with open(newhgrcpath, 'w') as newhgrc:
            with open(hgrcpath, 'r') as hgrc:
                section = None
                for line in hgrc:
                    sline = line.strip()

                    if sline.startswith('#'): # comment
                        newhgrc.write(line)
                        continue

                    if updated.get(section): # check updates
                        parsed = sline.split('=')
                        if len(parsed) == 2:
                            key, val = parsed[0].strip(), parsed[1].strip()
                            newval = updated[section].get(key)
                            if newval: # update
                                newhgrc.write('%s = %s\n' % (key, newval))
                                continue

                    if sline.startswith('['): # new section
                        # handle new entries while in the previous section
                        if entries.get(section):
                            for key, val in list(entries[section].items()):
                                newhgrc.write('%s = %s\n' % (key, val))
                            newhgrc.write('\n')
                            entries.pop(section)
                        section = sline[1:-1]

                    newhgrc.write(line)

            # unprocessed entries
            if entries:
                for key, val in list(entries[section].items()):
                    newhgrc.write('%s = %s\n' % (key, val))
                    newhgrc.write('\n')

        # show changes
        with open(hgrcpath, 'r') as hgrc:
            with open(newhgrcpath, 'r') as newhgrc:
                diff = tuple(unified_diff(hgrc.readlines(), newhgrc.readlines(),
                                          hgrcpath, newhgrcpath))
        for line in diff:
            self.ui.write(line)

        if not self.conf.opts.get('apply'):
            os.unlink(newhgrcpath)
            return ()

        if os.name == 'nt': # atomic rename not a windows thing
            os.unlink(hgrcpath)
        os.rename(newhgrcpath, hgrcpath)
        return diff

    def files(self, opts):
        """return managed files in the working directory"""
        u = self.ui._ui.copy()
        paths = []
        u.write = paths.append
        commands.files(self.ui._ui, self.repo, **opts)
        return paths


class zipit(archival.zipit):
    """Write archive to zip file or stream. Can write uncompressed,
    or compressed with deflate."""
    def __init__(self, dest, mtime, compress=True):
        if not isinstance(dest, str):
            try:
                dest.tell()
            except (AttributeError, IOError):
                dest = archival.tellable(dest)
        self.z = archival.zipfile.ZipFile(dest, 'a',
                                          compress and archival.zipfile.ZIP_DEFLATED or
                                          archival.zipfile.ZIP_STORED
        )
        # Python's zipfile module emits deprecation warnings if we try
        # to store files with a date before 1980.
        epoch = 315532800 # calendar.timegm((1980, 1, 1, 0, 0, 0, 1, 1, 0))
        if mtime < epoch:
            mtime = epoch
        self.mtime = mtime
        self.date_time = archival.time.gmtime(mtime)[:6]
