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
    'version': '0.1.2',
    'description': 'Python module for the DFN-PKI soap API',
    'long_description': "# DFN-PKI-Client\n\n## Example\n\n```\n#!/usr/bin/env python\n\nfrom dfn_pki_client.public_service import PublicServicePKI\nfrom dfn_pki_client.registration_service import RegistrationService\nfrom dfn_pki_client.utils import get_wsdl\n\n\ndef main():\n\n    pki = PublicServicePKI('config.ini')\n\n    ca_info = pki.get_ca_info(42)\n\n    print(ca_info)\n\n\nif __name__ == '__main__':\n    main()\n\n```\n\n## Installation\n\n### Linux (e.g. Ubuntu)\n\n    apt install openssl rustc\n    pip3 install cryptography pyopenssl suds-community urllib3\n\n### macOS\n\n    brew install openssl swig rustup\n    pip3 install cryptography pyopenssl suds-community urllib3\n\n### Windows (untested)\n\n    pip3 install cryptography pyopenssl suds-community urllib3\n\n\n## Setup\n\nCreate the configuration file ``config.ini``\n\n```\n[default]\ncert = file_name.p12\npassword = 0123456789\npublic_wsdl = https://pki.pca.dfn.de/<ca_name>/cgi-bin/pub/soap?wsdl=1\nregistration_wsdl = https://ra.pca.dfn.de/<ca_name>/cgi-bin/ra/soap?wsdl=1\ndomain_wsdl = https://ra.pca.dfn.de/<ca_name>/cgi-bin/ra/soap/DFNCERT/Domains?wsdl=1'\n```\n",
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
