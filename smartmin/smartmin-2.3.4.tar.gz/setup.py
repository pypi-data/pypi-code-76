# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['smartmin',
 'smartmin.csv_imports',
 'smartmin.csv_imports.migrations',
 'smartmin.management',
 'smartmin.management.commands',
 'smartmin.templatetags',
 'smartmin.users',
 'smartmin.users.migrations']

package_data = \
{'': ['*'],
 'smartmin': ['static/*',
              'static/css/*',
              'static/fonts/*',
              'static/img/*',
              'static/img/smartmin/*',
              'static/js/*',
              'static/js/libs/*',
              'templates/*',
              'templates/csv_imports/*',
              'templates/smartmin/*',
              'templates/smartmin/users/*']}

install_requires = \
['Django<3.0',
 'celery<5.0',
 'pytz',
 'redis>=2.10.5,<3.0.0',
 'sqlparse>=0.4.1,<0.5.0',
 'xlrd>=2.0.1,<3.0.0',
 'xlwt>=1.3.0,<2.0.0']

setup_kwargs = {
    'name': 'smartmin',
    'version': '2.3.4',
    'description': 'Scaffolding system for Django object management.',
    'long_description': "Django Smartmin\n===============\n\n[![Build Status](https://github.com/nyaruka/smartmin/workflows/CI/badge.svg)](https://github.com/nyaruka/smartmin/actions?query=workflow%3ACI) \n[![codecov](https://codecov.io/gh/nyaruka/smartmin/branch/master/graph/badge.svg)](https://codecov.io/gh/nyaruka/smartmin)\n[![PyPI Release](https://img.shields.io/pypi/v/smartmin.svg)](https://pypi.python.org/pypi/smartmin/)\n\nSmartmin was born out of the frustration of the Django admin site not being well suited to being exposed to clients. \nIt aims to allow you to quickly build scaffolding which you can customize by using Django views.\n\nIt is very opinionated in how it works, if you don't agree, Smartmin may not be for you:\n\n- Permissions are used to gate access to each page, embrace permissions throughout and you'll love this\n- CRUDL operations at the object level, that is, Create, Read, Update, Delete and List, permissions and views are based \n  around this\n- URL automapping via the the CRUDL objects, this should keep things very very DRY\n\nAbout Versions\n==============\n\nSmartmin tries to stay in lock step with the latest Django versions. With each new Django version a new Smartmin version \nwill be released and we will save the major changes (possibly breaking backwards compatibility) on these versions.  This \nincludes updating to the latest version of Twitter Bootstrap.\n\nThe latest version is the 2.2.* series which supports the Django 2.1.* and 2.2.* releases series.\n\nAbout\n=====\n\nThe full documentation can be found at: http://readthedocs.org/docs/smartmin/en/latest/\n\nThe official source code repository is: http://www.github.com/nyaruka/smartmin/\n\nBuilt in Rwanda by [Nyaruka Ltd](http://www.nyaruka.com).\n",
    'author': 'Nyaruka Ltd',
    'author_email': 'code@nyaruka.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
