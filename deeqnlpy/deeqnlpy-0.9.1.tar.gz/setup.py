# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deeqnlpy',
 'deeqnlpy.lib.baikal',
 'deeqnlpy.lib.baikal.language',
 'deeqnlpy.lib.google.api']

package_data = \
{'': ['*']}

install_requires = \
['grpcio==1.35.0', 'protobuf==3.14.0']

setup_kwargs = {
    'name': 'deeqnlpy',
    'version': '0.9.1',
    'description': 'The deeq nlp python client library',
    'long_description': None,
    'author': 'Gihyun YUN',
    'author_email': 'gih2yun@baikal.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://baikal.ai/app2/#/morpheme',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
