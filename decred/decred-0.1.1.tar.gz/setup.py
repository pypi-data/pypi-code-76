# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['decred',
 'decred.btc.nets',
 'decred.crypto',
 'decred.crypto.secp256k1',
 'decred.dcr',
 'decred.dcr.nets',
 'decred.dcr.wire',
 'decred.util',
 'decred.wallet']

package_data = \
{'': ['*'], 'decred.dcr': ['assets/*']}

install_requires = \
['appdirs>=1.4.3,<2.0.0',
 'base58>=2.0.0,<3.0.0',
 'blake256>=0.1.1,<0.2.0',
 'pynacl>=1.3.0,<2.0.0',
 'websocket_client>=0.57.0,<0.58.0']

setup_kwargs = {
    'name': 'decred',
    'version': '0.1.1',
    'description': 'A Python 3 Decred toolkit.',
    'long_description': None,
    'author': 'Brian Stafford',
    'author_email': 'buck@decred.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://decred.org/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
