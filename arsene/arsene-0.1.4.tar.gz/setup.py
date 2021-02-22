# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arsene', 'arsene.schemas']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7.3,<2.0.0']

extras_require = \
{'redis': ['redis>=3.5.3,<4.0.0']}

setup_kwargs = {
    'name': 'arsene',
    'version': '0.1.4',
    'description': 'Easy data cache management',
    'long_description': '# Cobnut\n[![Test](https://github.com/JeremyAndress/cobnut/actions/workflows/python-app.yml/badge.svg)](https://github.com/JeremyAndress/cobnut/actions/workflows/python-app.yml) [![license](https://img.shields.io/github/license/peaceiris/actions-gh-pages.svg)](LICENSE)\n\nSimple cache management to make your life easy.\n\n### Requirements \n- Python 3.6+ \n\n### Installation\n```sh\npip install cobnut\n```\n\n### Quick Start\nFor the tutorial, you must install redis as dependency\n\n```sh\npip install cobnut[redis]\n```\n\n\nThe simplest Cobnut setup looks like this:\n\n```python\nfrom cobnut import Cobnut, RedisModel\n\ncobnut = Cobnut(redis_connection=RedisModel(host="localhost"))\ncobnut.set(key=\'mykey\', data=\'mydata\')\ncobnut.get(key=\'mykey\')\n# Response: mydata\n\ncobnut.delete(key=\'mykey\')\ncobnut.get(key=\'mykey\')\n# Response: None\n\n```',
    'author': 'JeremyAndress',
    'author_email': 'jeremysilvasilva@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JeremyAndress/cobnut',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
