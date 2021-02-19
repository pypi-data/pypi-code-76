# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qcware_transpile',
 'qcware_transpile.dialects',
 'qcware_transpile.dialects.pyzx',
 'qcware_transpile.dialects.qiskit',
 'qcware_transpile.dialects.quasar',
 'qcware_transpile.translations',
 'qcware_transpile.translations.pyzx',
 'qcware_transpile.translations.pyzx.to_quasar',
 'qcware_transpile.translations.qiskit',
 'qcware_transpile.translations.qiskit.to_quasar',
 'qcware_transpile.translations.quasar',
 'qcware_transpile.translations.quasar.to_pyzx',
 'qcware_transpile.translations.quasar.to_qiskit']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.3.0,<21.0.0',
 'icontract>=2.4.1,<3.0.0',
 'pyrsistent>=0.17.3,<0.18.0',
 'toolz>=0.11.1,<0.12.0']

extras_require = \
{'pyzx': ['pyzx>=0.6.3,<0.7.0'],
 'qcware-quasar': ['qcware-quasar>=1.0.2,<2.0.0'],
 'qiskit': ['qiskit-aer>=0.7.2,<0.8.0']}

setup_kwargs = {
    'name': 'qcware-transpile',
    'version': '0.1.1a7',
    'description': 'A quantum circuit transpilation framework',
    'long_description': None,
    'author': 'Vic Putz',
    'author_email': 'vic.putz@qcware.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
