# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qiskit_qcware']

package_data = \
{'': ['*']}

install_requires = \
['icontract>=2.4.1,<3.0.0',
 'qcware-quasar>=1.0.1,<2.0.0',
 'qcware-transpile>=0.1.1.alpha.6,<0.2.0',
 'qcware>=3.0,<4.0',
 'qiskit-terra>=0.16.3,<0.17.0']

setup_kwargs = {
    'name': 'qiskit-qcware',
    'version': '0.1.1a5',
    'description': 'A provider for Qiskit providing QCWare Forge services',
    'long_description': None,
    'author': 'Vic Putz',
    'author_email': 'vic.putz@qcware.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
