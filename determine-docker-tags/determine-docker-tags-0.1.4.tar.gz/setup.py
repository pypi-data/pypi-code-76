# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['determine_docker_tags']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['determine-docker-tags = '
                     'determine_docker_tags.__init__:main']}

setup_kwargs = {
    'name': 'determine-docker-tags',
    'version': '0.1.4',
    'description': 'A small program to determine docker image tags',
    'long_description': '# docker-determine-tags\n\nA python program used to determine which docker tags should be applied to a docker image depending on various factors. This is mainly intended to be used together with Drone CI to automatically figure out version tags before build the container image.\n',
    'author': 'Magnus Walbeck',
    'author_email': 'magnus.walbeck@walbeck.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://git.walbeck.it/walbeck-it/determine-docker-tags',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
