# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sansio_lsp_client']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7.3,<2.0.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8']}

setup_kwargs = {
    'name': 'sansio-lsp-client',
    'version': '0.9.0',
    'description': 'An implementation of the client side of the LSP protocol, useful for embedding easily in your editor.',
    'long_description': '# sansio-lsp-client\n\nAn implementation of the client side of the LSP protocol, useful for embedding\neasily in your editor.\n',
    'author': 'Purple Myst',
    'author_email': 'PurpleMyst@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PurpleMyst/sansio-lsp-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
