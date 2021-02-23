"""maintenance of mercurial repository trees made easy

The full documentation is available online at https://hg.sr.ht/~auc/confman
or in the REAMDE.md file.
"""
testedwith = '4.6 4.7 4.8 5.0 5.1 5.2 5.3 5.4 5.5 5.6 5.7'

import os.path as osp
from mercurial import extensions

from .meta import colortable

from .commands import *


def extsetup(ui):
    """ add confman support to hgview """
    try:
        extensions.find(b'hgview')
    except KeyError:
        return
    try:
        from hgviewlib.util import SUBREPO_GETTERS
    except ImportError:
        return
    def _get_confman(repo_path):
        """ return mapping of section -> path
        for all managed repositories """
        confpath = osp.join(repo_path, '.hgconf')
        if not osp.exists(confpath):
            return None
        from .configuration import configurationmanager
        confman = configurationmanager(ui, repo_path, (), {})
        return ((section, conf.get('layout'))
                for section, conf, managed in confman.iterrepos()
                if (managed is not None or
                    conf.get('expand', None) is not None))
    SUBREPO_GETTERS.append(_get_confman)



