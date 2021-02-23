"""
guestrepo extension compatibility support
"""
import os
from mercurial import config, util, error

from .utils import ending
from .configuration import configurationmanager as _configurationmanager


class configurationmanager(_configurationmanager):
    "Configuration manager for guestrepo files"

    def readsnapshot(self):
        """ return a dict(layout:rev) using the guestrepo
        configuration files """
        grepopath = os.path.join(self.rootpath, '.hgguestrepo')
        if os.path.exists(grepopath):
            conf = config.config()
            conf.read(grepopath.encode('utf-8'))
            layouts = conf[b'']
            return {
                layout.decode('utf-8'): track.split()[1].decode('utf-8')
                for layout, track in layouts.items()
            }

        return {}

    def save_gently(self, tagmap):
        """gently rewrite the .hgconf updating only lines that need it

        :tagmap: a {section: track} dict
        :return: a list of rewritten (section, tracks)
        """
        # gently rewrite the .hgguestrepo ...
        basepath = os.path.dirname(self.rootpath)
        hgguestpath = os.path.join(self.rootpath, '.hgguestrepo')
        newhgguestpath = os.path.join(basepath, '.hgguestrepo.new')
        rewritten = []
        with open(newhgguestpath, 'w') as newhgguest:
            with open(hgguestpath, 'r') as hgguest:
                for lineno, sline in enumerate(hgguest):
                    line = sline.strip()
                    try:
                        layout, name_cset = line.split('=')
                        layout = layout.strip()
                        name_cset = name_cset.strip()
                        name, cset = name_cset.split(None, 1)
                        name = name.strip()
                        cset = cset.strip()
                    except:
                        raise error.Abort(b'Malformed line %s %r' % (lineno + 1, line))
                    track = tagmap.get(name)
                    if track is not None and cset != track:
                        sline = '%s = %s %s%s' % (layout, name, tagmap[name], ending(sline))
                        rewritten.append((name, track))
                    newhgguest.write(sline)
        if os.name == 'nt': # atomic rename not a windows thing
            os.unlink(hgguestpath)
        os.rename(newhgguestpath, hgguestpath)
        return rewritten
