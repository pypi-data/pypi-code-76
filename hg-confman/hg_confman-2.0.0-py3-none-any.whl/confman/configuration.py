"""This module contains the configurationmanager object."""

import os
import itertools
from collections import defaultdict

from mercurial import util, error
from .meta import MANDATORY, CONFMANENTRIES
from .utils import ending


def _filtersection(section, exactmatch=(), include=(), exclude=()):
    """True if the section may be processed"""
    exactmatch = exactmatch or ()
    include = include or ()
    exclude = exclude or ()
    _match = lambda section, matches: any(m in section for m in matches)

    if _match(section, exclude):
        return False
    if exactmatch:
        if _match(section, include) or section in exactmatch:
            return True
        return False
    if include:
        if _match(section, include):
            return True
        return False
    return True

STATUSMAP = {
    0: '   ',
    1: '\N{BOX DRAWINGS LIGHT VERTICAL}  ',
    2: '\N{BOX DRAWINGS LIGHT UP AND RIGHT}\N{RIGHTWARDS ARROW} ',
    3: '\N{BOX DRAWINGS LIGHT VERTICAL AND RIGHT}\N{RIGHTWARDS ARROW} '
    }


class configurationmanager(object):
    "Configuration manager"
    __slots__ = ('ui', 'rootpath', 'args', 'opts',
                 'confs', 'failed', 'sectionlevels')

    def __init__(self, ui, rootpath, args, opts):
        self.ui = ui
        self.rootpath = rootpath
        self.args = args
        self.opts = opts

        self.failed = set()
        self.sectionlevels = defaultdict(set)

        self._readconf()

    def _readconf(self):
        "Load configuration from <root>/.hgconf"
        from .utils import oconfig
        self.confs = oconfig(confman=self)
        self.confs.read(os.path.join(self.rootpath, '.hgconf'))

    def _check_parameters(self, section, skipmissing):
        "Validate configuration parameters"
        err = [opt for opt in MANDATORY if self.confs.get(section, opt) is None]
        if err:
            ui = self.ui
            if not skipmissing:
                ui.warn('You must complete the configuration before using it. See:\n')
                ui.warn(''.join('error: %s.%s is missing\n' % (section, opt) for opt in err))
                raise error.Abort(b'configuration error')
            else:
                ui.warn('%s is a partial override without its master entry\n' % section)
                return True

    def pathfromsection(self, section):
        "Return the path of the repository managed at ``section`` "
        rootpath = (self.opts.get('root_path') or
                    self.ui.configpath('confman', 'rootpath') or
                    self.rootpath)
        conf = self.confs[section]
        layout = conf['layout'].format(**conf)
        return os.path.join(rootpath, layout)

    def repofromsection(self, section):
        """Return hg.repository object managed at ``section`` or
        None if the repository is missing.
        Raise RepoError if the repository cannot be built."""
        from .managed import repoclassbyconf
        path = self.pathfromsection(section)
        if not os.path.exists(path):
            return None
        try:
            return repoclassbyconf(
                self.confs[section], path, self.opts.get('hggit')
            )(self, path)
        except error.RepoError:
            return None

    @property
    def sections(self):
        return self.confs.sections()

    def iterrepos(self, skipmissing=True):
        """Yield (section, conf, repository) for each managed
        repository. Repository may be None if it's missing. Skip
        bugged repositories.
        """
        include = set(self.opts.get('include_conf') or ())
        exclude = set(self.opts.get('exclude_conf') or ()) | self.failed
        exactmatch = set(self.args) or ()

        sections = self.sections
        isection = 0

        while isection < len(sections):
            section = sections[isection]
            isection += 1
            if not _filtersection(section, exactmatch, include, exclude):
                continue
            conf = self.confs[section]
            if self._check_parameters(section, skipmissing):
                continue
            managed = self.repofromsection(section)
            if managed is None and skipmissing:
                path = self.pathfromsection(section)
                self.ui.write('%s repository at "%s" not found\n' %
                              (section, path))
                continue
            yield section, conf, managed
            if conf.get('expand', None):
                self._readconf()
                sections = self.sections

    @property
    def urimap(self):
        mapfilepath = self.opts.get('uri_map_file')
        if not mapfilepath:
            return {}
        if not os.path.exists(mapfilepath):
            self.ui.warn('the %r uri map file cannot be found\n' % mapfilepath)
            return {}
        try:
            urimap = {}
            with open(mapfilepath, 'r') as mapfile:
                for line in mapfile:
                    line = line.strip()
                    if line.startswith('#') or line.startswith('['):
                        continue
                    try:
                        prefix, replacement = line.split('=')
                        prefix, replacement = prefix.strip(), replacement.strip()
                        urimap[prefix] = replacement
                    except:
                        raise error.ParseError('bad uri map')
            return urimap
        except error.ParseError:
            self.ui.warn('the %r uri map file looks malformed\n' % mapfilepath)
        return {}

    def rewriteuri(self, uri):
        for prefix, replacement in list(self.urimap.items()):
            if uri.startswith(prefix):
                newuri = uri.replace(prefix, replacement)
                return newuri
        return uri

    def fill_missing(self):
        "Try to clone the missing managed repositories if possible"
        from .managed import repoclassbyconf
        ui = self.ui
        # catches simple rev ids but NOT revexprs
        for section, conf, managed in self.iterrepos(skipmissing=False):
            if managed is not None:
                continue

            dest = self.pathfromsection(section)
            if not os.path.exists(dest):
                os.makedirs(dest)
            source = conf['pulluri'].format(**conf)
            ui.status('cloning %s from %s to %s\n' % (section, source, dest))
            try:
                path = self.pathfromsection(section)
                repoclassbyconf(
                    conf, path, self.opts.get('hggit')
                ).clone(
                    self, source, dest, self.confs[section]
                )
            except Exception as err:
                # the clone operation did fail
                self.failed.add(section)
                ui.write('%s\n' % err, label='confman.dirty')
                ui.debug(str(err))
                continue

            # if managed is a sub configuration, we add the rootpath
            # to its hgrc which allows to work from the managed confman
            if conf.get('expand') is not None:
                frompath = os.path.join(dest, '.hg')
                key = 'hgrc.confman.rootpath'
                if key in conf:
                    ui.info('there is already a %s' % key)
                conf[key] = os.path.relpath(self.rootpath, frompath)
            if set(conf) - set(CONFMANENTRIES):
                # let's write down those options
                self.handle_hgrc(section, conf)


    @util.cachefunc
    def levelstatus(self, section, level):
        sectionlevels = self.sectionlevels[section]
        sections = self.sections
        # sections under scope of the current section
        scope = sections[sections.index(section) + 1:]
        # levels where scoped sessions  are
        scopelevels = set(itertools.chain(*(
            self.sectionlevels[s] for s in scope)))

        if level not in sectionlevels:
            if level in scopelevels:
                return 1 # under our scope, not our business
            return 0 # out of scope
        nextsection = (section != sections[-1]
                       and sections[sections.index(section)+1]
                       or None)
        if nextsection:
            if not self.levelstatus(nextsection, level):
                return 2 # end of scope
            return 3 # we *override* this
        return 2 # end of scope

    def unicodetreenode(self, section):
        "Return the unicode string to print for the given section."
        # levels where current section is
        sectionlevels = self.sectionlevels[section]

        out = ''
        for level in range(max(sectionlevels) + 1):
            status = self.levelstatus(section, level)
            out += STATUSMAP[status]
        return out

    def handle_hgrc(self, section, conf):
        """Handler for the `hgrc` top level optional configuration entries
        Will turn any entry such as:
          hgrc.paths.foo = http://hg.bar.org
        into a foo entry in the managed repo hgrc [paths] section """
        from .utils import oconfig, _unflatten
        repopath = self.pathfromsection(section)
        hgrcpath = os.path.join(repopath, '.hg', 'hgrc')
        if not os.path.exists(hgrcpath):
            return
        config = oconfig(confman=self)
        config.read(hgrcpath)
        for toplevel, section_key_val in _unflatten(conf).items():
            if toplevel == 'hgrc':
                for section, key_val in section_key_val.items():
                    for key, val in key_val.items():
                        config.set(section, key, val)
        config.save(hgrcpath)

    def save(self, hgconfpath):
        "Save a new config to file hgconfpath"
        confs = self.confs.copy()
        with open(hgconfpath, 'w') as hgconf:
            for section in confs:
                conf = confs[section]
                hgconf.write('[%s]\n' % section)
                for attr in ('pulluri', 'layout', 'track'):
                    hgconf.write('%s = %s\n' % (attr, conf[attr]))
                hgconf.write('\n')

    def save_gently(self, tagmap):
        """gently rewrite the .hgconf updating only lines that need it

        :tagmap: a {section: track}
        :return: a list of rewritten (section, tracks)
        """
        hgconfpath = os.path.join(self.rootpath, '.hgconf')
        basepath = os.path.dirname(self.rootpath)
        newhgconfpath = os.path.join(basepath, '.hgconf.new')
        rewritten = []
        with open(newhgconfpath, 'w') as newhgconf:
            with open(hgconfpath, 'r') as hgconf:
                section = None
                for line in hgconf:
                    sline = line.strip()
                    if sline.startswith('['):
                        section = sline[1:-1]
                    elif sline.startswith('track') and section in tagmap:
                        line = 'track = %s%s' % (tagmap[section], ending(line))
                        rewritten.append((section, tagmap[section]))
                    newhgconf.write(line)

        if os.name == 'nt': # atomic rename not a windows thing
            os.unlink(hgconfpath)
        os.rename(newhgconfpath, hgconfpath)
        return rewritten

    def readsnapshot(self):
        "Return a {layout:rev} dict from a snapshot file"
        snappath = os.path.join(self.rootpath, '.hgsnap')
        if os.path.exists(snappath):
            with open(snappath, 'r') as snapfile:
                return {
                    layout: revision.strip()
                    for revision, layout in (
                            line.split() for line in snapfile
                    )
                }
        return {}

    def snapshot(self):
        "DEPRECATED. Do not use."
        ui = self.ui
        ui.write('`hg snapshot` is deprecated, see `hg cfbaseline`\n')

        if not os.path.exists(os.path.join(self.rootpath, '.hgsnap')):
            ui.status('populating .hgsnap for the first time\n')

        if self.opts['include_conf']:
            snaps = self.readsnapshot()
        else:
            snaps = {}
        unclean = []
        for section, conf, managed in self.iterrepos():
            path = conf['layout']
            if managed.check_dirty(section):
                unclean.append(section)
            ctx = managed.repo[None]
            node = ctx.p1().hex().decode('utf-8')
            snaps[path] = node

        if unclean:
            ui.warn('some repositories (%s) are unclean\n' % ', '.join(unclean))

        oldsnaps = self.readsnapshot()
        if oldsnaps != snaps:
            with open(os.path.join(self.rootpath, '.hgsnap'), 'w') as hgsnapfile:
                hgsnapfile.write(''.join('%s %s\n' % (node, path)
                                         for path, node in sorted(snaps.items())))
            ui.status('new snapshot in .hgsnap\n')
        else:
            ui.status('nothing changed\n')
