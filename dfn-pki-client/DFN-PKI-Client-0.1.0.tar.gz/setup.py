# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dfn_pki_client']

package_data = \
{'': ['*']}

modules = \
['README', 'config.ini']
install_requires = \
['click>=7.1.2,<8.0.0',
 'cryptography>=3.4.5,<4.0.0',
 'pyOpenSSL>=20.0.1,<21.0.0',
 'suds-community>=0.8.4,<0.9.0',
 'urllib3>=1.26.3,<2.0.0']

entry_points = \
{'console_scripts': ['trackdownchanges = dfn_pki_client.main:main']}

setup_kwargs = {
    'name': 'dfn-pki-client',
    'version': '0.1.0',
    'description': 'Python module for the DFN-PKI soap API',
    'long_description': None,
    'author': 'Robert Grätz',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ikreb7/DFN-PKI-Client',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
