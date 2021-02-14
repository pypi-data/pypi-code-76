# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ssb_client', 'ssb_client.feed', 'ssb_client.tests']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'secret-handshake>=0.1.0-alpha.3,<0.2.0']

setup_kwargs = {
    'name': 'ssb-client',
    'version': '0.1.0',
    'description': 'Client for Secure Scuttlebutt (SSB)',
    'long_description': '# Secure Scuttlebutt (SSB) Client in Python\n\n**WORK IN PROGRESS**\n\nThis is a fork of the unmaintained [pyssb repo](https://github.com/pferreir/pyssb).\n\nThings that are currently implemented:\n\n * Basic Message feed logic\n * Secret Handshake\n * packet-stream protocol\n\nUsage (requires [Poetry](https://python-poetry.org/)):\n\n```\npoetry install\nPYTHONPATH=. poetry run python3 examples/test_client.py\n```\n',
    'author': 'Henning Jacobs',
    'author_email': 'henning@jacobs1.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://codeberg.org/hjacobs/python-ssb-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
