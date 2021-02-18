# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['apologiesserver']

package_data = \
{'': ['*']}

install_requires = \
['apologies>=0.1.29,<0.2.0',
 'asyncio-periodic>=2019.2,<2020.0',
 'ordered-set>=4.0.1,<5.0.0',
 'websockets>=8.1,<9.0']

entry_points = \
{'console_scripts': ['apologies-server = apologiesserver.scripts:server']}

setup_kwargs = {
    'name': 'apologiesserver',
    'version': '0.1.19',
    'description': 'Websocket server to interactively play the Apologies game',
    'long_description': '# Apologies Server\n\n[![pypi](https://img.shields.io/pypi/v/apologiesserver.svg)](https://pypi.org/project/apologiesserver/)\n[![license](https://img.shields.io/pypi/l/apologiesserver.svg)](https://github.com/pronovic/apologies-server/blob/master/LICENSE)\n[![wheel](https://img.shields.io/pypi/wheel/apologiesserver.svg)](https://pypi.org/project/apologiesserver/)\n[![python](https://img.shields.io/pypi/pyversions/apologiesserver.svg)](https://pypi.org/project/apologiesserver/)\n[![Test Suite](https://github.com/pronovic/apologies-server/workflows/Test%20Suite/badge.svg)](https://github.com/pronovic/apologies-server/actions?query=workflow%3A%22Test+Suite%22)\n[![docs](https://readthedocs.org/projects/apologies-server/badge/?version=stable&style=flat)](https://apologies-server.readthedocs.io/en/stable/)\n[![coverage](https://coveralls.io/repos/github/pronovic/apologies-server/badge.svg?branch=master)](https://coveralls.io/github/pronovic/apologies-server?branch=master)\n\n[Apologies Server](https://github.com/pronovic/apologies-server) is a [Websocket](https://en.wikipedia.org/wiki/WebSocket) server interface used to interactively play a multi-player game using the [Apologies](https://github.com/pronovic/apologies) library.  The Apologies library implements a game similar to the [Sorry](https://en.wikipedia.org/wiki/Sorry!_(game)) board game.  \n\nIt was written as a learning exercise and technology demonstration effort, and serves as a complete example of how to manage a modern (circa 2020) Python project, including style checks, code formatting, integration with IntelliJ, [CI builds at GitHub](https://github.com/pronovic/apologies-server/actions), and integration with [PyPI](https://pypi.org/project/apologiesserver/) and [Read the Docs](https://apologies-server.readthedocs.io/en/stable/).  \n\nSee the [documentation](https://apologies-server.readthedocs.io/en/stable/design.html) for notes about the public interface and the event model.\n\nAs of this writing, the published PyPI project does not include a script to run\nthe server. The only way to run it is from the codebase, for local testing. See\nthe [developer](https://github.com/pronovic/apologies-server/blob/master/DEVELOPER.md#running-the-server) documentation\nat GitHub for more information.\n\nAs a technology demonstration effort, the Apologies Server is fairly\nsimplistic.  It runs as a single stateful process that maintains game state in\nmemory.  It cannot be horizontally scaled, and there is no option for an\nexternal data store.  There is also only limited support for authentication and\nauthorization - any player can register any handle that is not currently being\nused.  We do enforce resource limits (open connections, registered users,\nin-progress games) to limit the amount of damage abusive clients can do.\n',
    'author': 'Kenneth J. Pronovici',
    'author_email': 'pronovic@ieee.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/apologiesserver/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
