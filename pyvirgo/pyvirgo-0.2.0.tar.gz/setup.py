# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['virgo']

package_data = \
{'': ['*']}

install_requires = \
['ply>=3.11,<4.0']

setup_kwargs = {
    'name': 'pyvirgo',
    'version': '0.2.0',
    'description': 'A Python package for the Virgo language',
    'long_description': '# PyVirgo\n\nThis is a Python implementation of Virgo, the graph declarative language.\n\nYou can find details of Virgo with the Go implementation at https://github.com/r2d4/virgo\n\nVirgo is designed so that we can express graphs in a config file. These could be dependency graphs, for example of a build process, or any other graph structure.\n\nTo invoke PyVirgo:\n>>> import virgo\n>>> g = virgo.loads("a -> b, c <- d")\n>>> g       # doctest: +ELLIPSIS\n<virgo.graph.Graph object at ...>\n>>> sorted(list(g.direct_successors_of("a")))\n[\'b\', \'c\']\n\nIt\'s more likely that we will want to load a graph from a file:\n>>> g2 = virgo.load("test/files/make.vgo")\n>>> g2      # doctest: +ELLIPSIS\n<virgo.graph.Graph object at ...>\n>>> g2.direct_successors_of("src files")\n{\'test\'}\n\nWe can access the \'node data\' for each node, by identifier.\n>>> g2.nodes["src files"]\n\'go build ./...\'\n',
    'author': 'Jack Grahl',
    'author_email': 'jack.grahl@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jwg4/pyvirgo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
