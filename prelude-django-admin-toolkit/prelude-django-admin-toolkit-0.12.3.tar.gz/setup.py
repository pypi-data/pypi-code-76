# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prelude_django_admin_toolkit',
 'prelude_django_admin_toolkit.migrations',
 'prelude_django_admin_toolkit.templatetags']

package_data = \
{'': ['*'],
 'prelude_django_admin_toolkit': ['locale/pt_BR/LC_MESSAGES/*',
                                  'static/*',
                                  'static/prelude_django_admin_toolkit/*',
                                  'static/prelude_django_admin_toolkit/css/*',
                                  'static/prelude_django_admin_toolkit/icon/*',
                                  'static/prelude_django_admin_toolkit/js/*',
                                  'templates/admin/*',
                                  'templates/admin/auth/user/*',
                                  'templates/admin/edit_inline/*',
                                  'templates/admin/includes/*',
                                  'templates/admin/pages/*',
                                  'templates/admin/widgets/*',
                                  'templates/registration/*']}

install_requires = \
['django>=3,<4']

setup_kwargs = {
    'name': 'prelude-django-admin-toolkit',
    'version': '0.12.3',
    'description': 'An alternative Django Admin theme with Batteries; project Bruh',
    'long_description': None,
    'author': 'Jonhnatha Trigueiro',
    'author_email': 'joepreludian@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
