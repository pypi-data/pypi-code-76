# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jnt_django_toolbox',
 'jnt_django_toolbox.admin',
 'jnt_django_toolbox.admin.decorators',
 'jnt_django_toolbox.admin.fields',
 'jnt_django_toolbox.admin.filters',
 'jnt_django_toolbox.admin.helpers',
 'jnt_django_toolbox.admin.widgets',
 'jnt_django_toolbox.consts',
 'jnt_django_toolbox.context_managers',
 'jnt_django_toolbox.decorators',
 'jnt_django_toolbox.forms',
 'jnt_django_toolbox.forms.fields',
 'jnt_django_toolbox.helpers',
 'jnt_django_toolbox.management',
 'jnt_django_toolbox.management.commands',
 'jnt_django_toolbox.models',
 'jnt_django_toolbox.models.fields',
 'jnt_django_toolbox.models.fields.bit',
 'jnt_django_toolbox.profiling',
 'jnt_django_toolbox.profiling.db',
 'jnt_django_toolbox.profiling.decorators',
 'jnt_django_toolbox.profiling.profilers']

package_data = \
{'': ['*']}

install_requires = \
['dateparser', 'django>=3']

extras_require = \
{'jaeger': ['jaeger-client']}

setup_kwargs = {
    'name': 'jnt-django-toolbox',
    'version': '0.1.52',
    'description': '',
    'long_description': None,
    'author': 'Junte',
    'author_email': 'tech@junte.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
