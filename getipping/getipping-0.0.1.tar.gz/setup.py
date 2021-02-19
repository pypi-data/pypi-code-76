# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['getipping']
setup_kwargs = {
    'name': 'getipping',
    'version': '0.0.1',
    'description': 'Do you want to know the ip or ping? If yes, then write this country and find out the ip site: getip.ip ("site.site", port). If you want to see the ping enter this line: getip.ping ("site.site")',
    'long_description': None,
    'author': 'TikOt Studio',
    'author_email': 'tikotstudio@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
