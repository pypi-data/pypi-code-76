# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['tikotapi']
setup_kwargs = {
    'name': 'tikotapi',
    'version': '1.0.0',
    'description': 'API by TikOt. Connect to account (testing account): tikotapi.connect(). Next to dashboard: tikotapi.panel_service (panel_tikotshop)("login", "password").',
    'long_description': None,
    'author': 'tikotstudio',
    'author_email': 'tikotstudio@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
