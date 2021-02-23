"This module contains useful stuff to play with repository specs"

import os
import errno
import codecs
from collections import defaultdict
import urllib.request, urllib.parse, urllib.error
import contextlib

from mercurial import util, hg, error
from mercurial.config import config, _
from .hgcompat import compilere

from .meta import CONFMANENTRIES

def ending(line):
    "Return the newline character(s) of the line."
    if line.endswith('\r\n'):
        return '\r\n'
    elif line.endswith('\r'):
        return '\r'
    else:
        return '\n'

# configuration handling

def _compilere(pattern):
    "Compile regexp (pattern + '$')"
    return compilere(pattern + '$')


class WrappedRepo:

    def __init__(self, repo):
        if isinstance(repo, WrappedRepo):
            repo = repo._repo
        self._repo = repo

    def __getattr__(self, name):
        if name in ('root', 'path', 'sharedpath'):
            thing = getattr(self._repo, name)
            if isinstance(thing, bytes):
                return thing.decode('utf-8')
            return thing
        return getattr(self._repo, name)

    def __getitem__(self, name):
        return self._repo[name]

    def __len__(self):
        return len(self._repo)


class WrappedUI:

    def __init__(self, ui):
        if isinstance(ui, WrappedUI):
            ui = ui._ui
        self._ui = ui

    def _output(self, meth, *a, label=b'', **k):
        if label:
            label = label.encode('utf-8')
        return meth(
            *(elt.encode('utf-8')
              if isinstance(elt, str) else elt
              for elt in a),
            label=label,
            **k
        )

    def write(self, *a, label=b'', **k):
        return self._output(
            self._ui.write,
            *a, label=label, **k
        )

    def status(self, *a, label=b'', **k):
        return self._output(
            self._ui.status,
            *a, label=label, **k
        )

    def warn(self, *a, label=b'', **k):
        return self._output(
            self._ui.warn,
            *a, label=label, **k
        )

    def error(self, *a, label=b'', **k):
        return self._output(
            self._ui.error,
            *a, label=label, **k
        )

    def configpath(self, *args, **kw):
        args = (
            elt.encode('utf-8')
            if isinstance(elt, str) else elt
            for elt in args
        )
        path = self._ui.configpath(*args, **kw)
        if path is not None:
            return path.decode('utf-8')

    def write_bytes(self, *a, label=b'', **k):
        return self._ui.write(*a, label=label, **k)

    def __getattr__(self, name):
        return getattr(self._ui, name)


class sectionfilter(object):
    "Callable that returns True if the section is included, else False"
    rewhitelist = ()
    reblacklist = ()
    whitelist = ()
    blacklist = ()

    def __init__(self, regexp=False, parent=None, morewhite=(), moreblack=()):
        """
        :regexp: booleen defining is ``morewhite`` and ``moreblack``
                 contains regular exprexions
        :parent: the filtersection object of the parent configuration
        :moreblack: additional (merged with parent list) white sections
        :moreblack: additional (merged with parent list) black sections
        """
        self.regexp = regexp
        if parent:
            self.rewhitelist = parent.rewhitelist
            self.reblacklist = parent.reblacklist
            self.whitelist = parent.whitelist
            self.blacklist = parent.blacklist
        if regexp:
            self.rewhitelist = (self.rewhitelist +
                                tuple(_compilere(exp) for exp in morewhite))
            self.reblacklist = (self.reblacklist +
                                tuple(_compilere(exp) for exp in moreblack))
        else:
            self.whitelist = self.whitelist + morewhite
            self.blacklist = self.blacklist + moreblack

    def __call__(self, section):
        if (section in self.blacklist or
            any(re.match(section) for re in self.reblacklist)):
            return False
        if ((self.whitelist and section not in self.whitelist) or
            (self.rewhitelist and not any(re.match(section) for re in self.rewhitelist))):
            return False
        return True


class oconfig(object):
    "Identical to mercurial config but with ordered section."

    def __init__(self, orig=None, confman=None):
        if orig is None:
            self._data = {}
            self._source = {}
            self._unset = []
        else:
            self._data = dict(orig._data)
            self._source = orig._source.copy()
            self._unset = orig._unset[:]
            confman = orig.confman
        assert confman
        self.confman = confman

    def __contains__(self, section):
        return section in self._data

    def __getitem__(self, section):
        return self._data.get(section, {})

    def __iter__(self):
        for d in self.sections():
            yield d

    def get(self, section, item, default=None):
        return self._data.get(section, {}).get(item, default)

    def set(self, section, item, value, source=''):
        if section not in self:
            self._data[section] = {}
        self._data[section][item] = value
        if source:
            self._source[(section, item)] = source

    def copy(self):
        return oconfig(orig=self)

    def sections(self):
        "Return the list of section names."
        return list(self._data.keys())

    def save(self, hgrcpath):
        "Write the .hg/hgrc of a managed repo."
        with open(hgrcpath, 'w') as hgrc:
            for section in self:
                hgrc.write('[%s]\n' % section)
                for k, v in self[section].items():
                    hgrc.write('%s = %s\n' % (k, v))
                hgrc.write('\n')

    def parse(self, src, data, sections=None, remap=None, include=None,
              # PATCH: level and filtering
              level=0, section_filter=None):
        sectionre = compilere(r'\[([^\[]+)\]')
        itemre = compilere(r'([^=\s][^=]*?)\s*=\s*(.*\S|)')
        # PATCH
        expandre = compilere(r'(expand)(\.whitelist|\.blacklist|)(\.re|)\s*=\s*(.*)$')
        # /PATCH
        contre = compilere(r'\s+(\S|\S.*\S)\s*$')
        emptyre = compilere(r'(;|#|\s*$)')
        commentre = compilere(r'(;|#)')
        unsetre = compilere(r'%unset\s+(\S+)')
        includere = compilere(r'%include\s+(\S|\S.*\S)\s*$')
        section = ""
        item = None
        line = 0
        cont = False
        # PATCH
        if section_filter is None:
            section_filter = sectionfilter()
        # /PATCH
        for l in data.splitlines(True):
            line += 1
            if line == 1 and l.startswith('\xef\xbb\xbf'):
                # Someone set us up the BOM
                l = l[3:]
            if cont:
                if commentre.match(l):
                    continue
                m = contre.match(l)
                if m:
                    if sections and section not in sections:
                        continue
                    v = self.get(section, item) + "\n" + m.group(1)
                    self.set(section, item, v, "%s:%d" % (src, line))
                    continue
                item = None
                cont = False
            m = includere.match(l)
            if m:
                inc = util.expandpath(m.group(1))
                base = os.path.dirname(src)
                inc = os.path.normpath(os.path.join(base, inc))
                if include:
                    try:
                        include(inc, remap=remap, sections=sections)
                    except IOError as inst:
                        if inst.errno != errno.ENOENT:
                            raise error.ParseError(_("cannot include %s (%s)")
                                                   % (inc, inst.strerror),
                                                   "%s:%s" % (src, line))
                continue
            if emptyre.match(l):
                continue
            m = sectionre.match(l)
            if m:
                section = m.group(1)
                # PATCH: filter section and section levels
                if remap:
                    section = remap.get(section, section)
                if not section_filter(section):
                    continue
                self.confman.sectionlevels[section].add(level)
                # /PATCH
                if section not in self:
                    self._data[section] = {}
                continue

            # PATCH: filter section
            if not section_filter(section):
                continue

            # PATCH: expand=
            m = expandre.match(l)
            if m:
                assert section
                path = self.confman.pathfromsection(section)
                inc = os.path.normpath(os.path.join(path, '.hgconf'))
                self.set(section, 'expand', 'confman', "%s:%d" % (src, line))
                if include:
                    morewhite = ()
                    moreblack = ()
                    if m.group(2) == '.whitelist':
                        morewhite = tuple(m.group(4).split())
                    elif m.group(2) == '.blacklist':
                        moreblack += tuple(m.group(4).split())
                    _section_filter = sectionfilter(regexp=bool(m.group(3)),
                                                    parent=section_filter,
                                                    morewhite=morewhite,
                                                    moreblack=moreblack)

                    try:
                        include(inc, remap=remap, sections=sections, level=level+1,
                                section_filter=_section_filter)
                    except IOError as inst:
                        if inst.errno != errno.ENOENT:
                            raise error.ParseError(_("cannot expand %s (%s)")
                                                   % (inc, inst.strerror),
                                                   "%s:%s" % (src, line))
                continue
            # /PATCH
            m = itemre.match(l)
            if m:
                item = m.group(1)
                cont = True
                if sections and section not in sections:
                    continue
                self.set(section, item, m.group(2), "%s:%d" % (src, line))
                continue
            m = unsetre.match(l)
            if m:
                name = m.group(1)
                if sections and section not in sections:
                    continue
                if self.get(section, name) is not None:
                    del self._data[section][name]
                self._unset.append((section, name))
                continue

            raise error.ParseError(
                l.rstrip().encode('utf-8'),
                ("%s:%s" % (src, line)).encode('utf-8')
            )

    def parse_guestrepo(self, dirpath, level=0, section_filter=None):
        "Parse guestrepo files in dirpath"
        # a guestrepo configuration is made of two files:
        # .hggrmapping and .hgguestrepo
        if section_filter is None:
            section_filter = sectionfilter()
        mappingpath = os.path.join(dirpath, '.hggrmapping')
        mappingconf = config()
        mappingconf.read(mappingpath.encode('utf-8'))
        section = None
        for section in mappingconf[b'']:
            if section_filter(section):
                self.set(
                    section.decode('utf-8'),
                    'pulluri',
                    mappingconf[b''][section].decode('utf-8')
                )
                self.confman.sectionlevels[section.decode('utf-8')].add(level)
        guestpath = os.path.join(dirpath, '.hgguestrepo')
        guestconf = config()
        guestconf.read(guestpath.encode('utf-8'))
        for layout in guestconf[b'']:
            section, cset = guestconf[b''][layout].split(None, 1)
            if section_filter(section):
                self.set(
                    section.decode('utf-8'),
                    'layout',
                    layout.decode('utf-8')
                )
                self.set(
                    section.decode('utf-8'),
                    'track',
                    cset.decode('utf-8')
                )

    def read(self, path, fp=None, sections=None, remap=None, **kwargs):
        if os.path.exists(path):
            if not fp:
                fp = util.posixfile(path)
            self.parse(path, fp.read(), sections, remap, self.read, **kwargs)
        else:
            # PATCH: try guestrepo
            dirpath = os.path.dirname(path)
            self.parse_guestrepo(dirpath, **kwargs)


def upwarditer(path):
    "Fonction generator that yield parents of path"
    while path:
        yield path
        path = os.path.dirname(path)
        if path in ('', '/'): # root, depending on linux/win32
            return

def findrootpath(ui, conffilename, startpath):
    "Find `conffilename` by changing directories upward"
    for iterations, repourl in enumerate(upwarditer(startpath)):
        confpath = os.path.join(repourl, conffilename)
        if os.path.exists(confpath):
            if iterations:
                if not ui.quiet:
                    ui.write('found configuration repo at %s\n' % repourl,
                             label='confman.updated')
            yield repourl
            raise StopIteration
        else:
            yield None
        iterations += 1


def readconf(ui, repo, args, opts):
    "Parse the configuration file into a config object."
    # prevent cyclic imports
    from . import gr
    from .configuration import configurationmanager
    for cmrootpath, grrootpath in zip(findrootpath(ui, '.hgconf', repo.root),
                                      findrootpath(ui, '.hgguestrepo', repo.root)):
        if cmrootpath:
            confman = configurationmanager(ui, cmrootpath, args, opts)
            break
        elif grrootpath:
            confman = gr.configurationmanager(ui, grrootpath, args, opts)
            break
    else:
        raise error.Abort(
            b'cannot find an .hgconf file in the path and '
            b'parents up to the root',
            hint=b'see hg help confman'
        )
    return confman, WrappedRepo(
        hg.repository(ui, confman.rootpath.encode('utf-8'))
    )

# dictionnaries operations

def _unflatten(flattened, skipkeys=CONFMANENTRIES, failed=None):
    """Build nested dictionaries from a flattened one, e.g
    hgrc.path.default-push -> {'hgrc': {'path': {'defaul-push': ...}}}
    """
    nested = defaultdict(lambda: defaultdict(dict))
    for key, value in flattened.items():
        if key in skipkeys:
            continue
        try:
            parts = [k.strip() for k in key.split('.')]
            toplevel, newsection, newkey = parts
        except ValueError:
            if failed is not None:
                failed.append('`%s` key cannot be handled' % key)
            continue
        nested[toplevel][newsection][newkey] = value
    return nested

# download utility

@contextlib.contextmanager
def download_file(source):
    """Download file at ``source``. This function manage file:// scheme"""
    u = urllib.parse.urlparse(source)
    if u.scheme == 'file':
        with open(os.path.join(*source[7:].split('/')), 'rb') as fp:
            yield fp
    else:
        import requests, tempfile
        req = requests.get(source, stream=True)
        with tempfile.TemporaryFile() as fp:
            for chunk in req.iter_content(chunk_size=4096):
                fp.write(chunk)
            fp.flush()
            fp.seek(0)
            yield fp


# register encoding error handlers

def _treegraph_unicode_encode_handler(error):
    """Unicode error handler for tree graph characters. Shall be given to
    codecs.register_error."""
    obj = error.object[error.start:error.end + 1]
    obj = obj.replace('\N{BOX DRAWINGS LIGHT VERTICAL}', '|') # │
    obj = obj.replace('\N{BOX DRAWINGS LIGHT VERTICAL AND RIGHT}', '|') # ├
    obj = obj.replace('\N{BOX DRAWINGS LIGHT UP AND RIGHT}', '`') # └
    obj = obj.replace('\N{RIGHTWARDS ARROW}', '-') # →
    return obj, error.end + 1
codecs.register_error('treegraph', _treegraph_unicode_encode_handler)

# a 'confman' encoding error handler

def _confman_unicode_encode_handler(error):
    obj = error.object[error.start:error.end + 1]
    obj = obj.replace('\N{CHECK MARK}', 'ok')
    obj = obj.replace('\N{MARRIAGE SYMBOL}', '[shared]')
    return obj, error.end
codecs.register_error('confman', _confman_unicode_encode_handler)
