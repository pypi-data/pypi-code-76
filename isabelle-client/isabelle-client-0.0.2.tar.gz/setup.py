# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['isabelle_client']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'isabelle-client',
    'version': '0.0.2',
    'description': 'A client to Isabelle proof assistant server',
    'long_description': '# Isabelle Client\n\nA client for [Isabelle](https://isabelle.in.tum.de) server. For more information about the server see part 4 of [the Isabelle system manual](https://isabelle.in.tum.de/dist/Isabelle2020/doc/system.pdf).\n',
    'author': 'Boris Shminke',
    'author_email': 'boris@shminke.ml',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/inpefess/isabelle-client',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
