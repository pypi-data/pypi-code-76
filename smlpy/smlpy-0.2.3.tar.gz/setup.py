# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['smlpy']

package_data = \
{'': ['*']}

install_requires = \
['jsons>=1.3.0,<2.0.0',
 'loguru>=0.5.3,<0.6.0',
 'pyserial-asyncio>=0.5,<0.6',
 'pyserial>=3.5,<4.0',
 'pyyaml>=5.3.1,<6.0.0',
 'typing-extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'smlpy',
    'version': '0.2.3',
    'description': 'smlpy enables reading of smart meter language (sml) data from a smart power meter. You need a working IR-reading device for this, e.g. https://shop.weidmann-elektronik.de/index.php?page=product&info=24which must be connected to an USB port. Please note that this library only supports a small part of the SML-spec, especially the sending part is intentionally omitted',
    'long_description': None,
    'author': 'christian.sauer',
    'author_email': 'christian.sauer@codecentric.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ChristianSauer/smlpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
