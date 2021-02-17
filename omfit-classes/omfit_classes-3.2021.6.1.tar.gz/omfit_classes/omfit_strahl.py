try:
    # framework is running
    from .startup_choice import *
except ImportError as _excp:
    # class is imported by itself
    if (
        'attempted relative import with no known parent package' in str(_excp)
        or 'No module named \'omfit_classes\'' in str(_excp)
        or "No module named '__main__.startup_choice'" in str(_excp)
    ):
        from startup_choice import *
    else:
        raise

from omfit_classes.omfit_ascii import OMFITascii

__all__ = ['OMFITstrahl']


class OMFITstrahl(SortedDict, OMFITascii):
    r"""
    OMFIT class used to interface with STRAHL input files

    :param filename: filename passed to OMFITobject class

    :param \**kw: keyword dictionary passed to OMFITobject class
    """

    def __init__(self, filename, **kw):
        SortedDict.__init__(self)
        OMFITascii.__init__(self, filename, **kw)
        self.dynaLoad = True

    @dynaLoad
    def load(self):
        with open(self.filename, 'r') as f:
            lines = f.readlines()
        cvs = -1
        for line in lines:
            if line.startswith('cv '):
                cvs += 1
                key = cvs
                self[key] = []

            self[key].append(line.strip())
        for key in self:
            name = re.sub(r'cv\s+(.*)', r'\1', self[key][0])
            value = ' '.join([_f for _f in self[key][1:] if _f])
            if not value.startswith("'") and ' ' in value:
                value = np.array(list(map(float, value.split(' '))))
                for item in ['Electron Density', 'Electron Temperature', 'Ion Temperature']:
                    if name.lower().startswith(item.lower()):
                        value = value[1:] * value[0]
                        break
            else:
                value = eval(value)
            self[key] = [name, value]

    def save(self):
        lines = []
        for key, value in list(self.values()):
            lines.append('cv    ' + key)
            if key == 'time-vector':
                for item in value:
                    lines.append('   %f' % item)
            elif isinstance(value, str):
                lines.append('   %s' % repr(value))
            else:
                tmp = value
                for item in ['Electron Density', 'Electron Temperature', 'Ion Temperature']:
                    if key.lower().startswith(item.lower()):
                        tmp = [value[0]] + tolist(value / value[0])
                        break
                lines.append('   %s' % ' '.join(map(str, tolist(tmp))))
            lines.extend(['', ''])
        pprint(lines)
        with open(self.filename, 'w') as f:
            f.write('\n'.join(lines))
