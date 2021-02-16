# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scimschema', 'scimschema._model', 'scimschema.core_schemas']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'scimschema',
    'version': '0.2.89',
    'description': 'A validator for System for Cross domain Identity Management (SCIM) responses given predefine schemas',
    'long_description': None,
    'author': 'Gordon So',
    'author_email': 'gordonkwso@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/GordonSo/scimschema',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
