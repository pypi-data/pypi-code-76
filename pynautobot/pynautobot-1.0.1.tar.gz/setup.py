# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pynautobot', 'pynautobot.core', 'pynautobot.models']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.20.0,<3.0.0']

setup_kwargs = {
    'name': 'pynautobot',
    'version': '1.0.1',
    'description': 'Nautobot API client library',
    'long_description': "# Pynautobot\nPython API client library for [Nautobot](https://github.com/nautobot-community/nautobot).\n\n\n## Installation\n\nTo install run `pip install pynautobot`.\n\nAlternatively, you can clone the repo and run `python setup.py install`.\n\n\n## Quick Start\n\nThe full pynautobot API is documented on [Read the Docs](http://pynautobot.readthedocs.io/en/latest/), but the following should be enough to get started using it.\n\nTo begin, import pynautobot and instantiate the API.\n\n```\nimport pynautobot\nnb = pynautobot.api(\n    'http://localhost:8000',\n    token='d6f4e314a5b5fefd164995169f28ae32d987704f'\n)\n```\n\nThe first argument the .api() method takes is the Nautobot URL. There are a handful of named arguments you can provide, but in most cases none are required to simply pull data. In order to write, the `token` argument should to be provided.\n\n\n## Queries\n\nThe pynautobot API is setup so that Nautobot's apps are attributes of the `.api()` object, and in turn those apps have attribute representing each endpoint. Each endpoint has a handful of verbs available to carry out actions on the endpoint. For example, in order to query all the objects in the devices endpoint you would do the following:\n\n```\nnb.dcim.devices.all()\n[test1-leaf1, test1-leaf2]\n```\n\n### Threading\n\npynautobot supports multithreaded calls (in Python 3 only) for `.filter()` and `.all()` queries. It is **highly recommended** you have `MAX_PAGE_SIZE` in your Nautobot install set to anything *except* `0` or `None`. The default value of `1000` is usually a good value to use. To enable threading, add `threading=True` parameter to the `.api`:\n\n```python\nnb = pynautobot.api(\n    'http://localhost:8000',\n    threading=True,\n)\n```\n",
    'author': 'Network to Code, LLC',
    'author_email': 'opensource@networktocode.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://nautobot.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
