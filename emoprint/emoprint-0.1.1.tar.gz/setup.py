# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['emoprint']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'emoprint',
    'version': '0.1.1',
    'description': "'The most uesless Python library ever' -- Cheuk 😅 Emoprint let you have more fun with your buildin print function by adding a random emoji to whatever you are printing!",
    'long_description': None,
    'author': 'Cheukting',
    'author_email': 'cheukting.ho@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
