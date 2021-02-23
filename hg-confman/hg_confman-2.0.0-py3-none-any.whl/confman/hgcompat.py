"""This version aims to ensure compatibility between multiple version of
mercurial.
"""
from mercurial.util import sortdict, re as hgre
from mercurial.configitems import coreconfigitem

compilere = hgre.compile

class sortdict(sortdict):

    def preparewrite(self):
        """call this before writes, return self or a copied new object"""
        if getattr(self, '_copied', 0):
            self._copied -= 1
            return self.__class__(self)
        return self

coreconfigitem(b'confman', b'rootpath',
               default=None
)


from mercurial import exchange
def push(local, remote, *args, **kwargs):
    return exchange.push(local, remote, *args, **kwargs)
def pull(local, remote, *args, **kwargs):
    return exchange.pull(local, remote, *args, **kwargs)


__all__ = ('sortdict', 'compilere')
