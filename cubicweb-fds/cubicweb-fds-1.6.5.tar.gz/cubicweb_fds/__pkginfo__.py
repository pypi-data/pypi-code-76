# pylint: disable=W0622
"""cubicweb-fds application packaging information"""

modname = 'fds'
distname = 'cubicweb-fds'

numversion = (1, 6, 5)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'
description = ''
web = 'https://www.cubicweb.org/project/%s' % distname

__depends__ = {
    'cubicweb': '>= 3.26.0',
    'six': '>= 1.12.O',
}
__recommends__ = {}

classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Programming Language :: JavaScript',
]
