# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['coreapi-stubs',
 'coreschema-stubs',
 'openapi_codec-stubs',
 'rest_framework-stubs',
 'rest_framework_swagger-stubs']

package_data = \
{'': ['*'],
 'coreapi-stubs': ['codecs/*'],
 'coreschema-stubs': ['encodings/*'],
 'rest_framework-stubs': ['authtoken/*',
                          'authtoken/management/*',
                          'authtoken/management/commands/*',
                          'management/commands/*',
                          'schemas/*',
                          'templatetags/*',
                          'utils/*']}

setup_kwargs = {
    'name': 'djangorestframework-types',
    'version': '0.4.0',
    'description': 'Type stubs for Django Rest Framework',
    'long_description': "# djangorestframework-types [![PyPI](https://img.shields.io/pypi/v/djangorestframework-types.svg)](https://pypi.org/project/djangorestframework-types/)\n\nType stubs for [Django Rest Framework](https://www.django-rest-framework.org).\n\n> Note: this project was forked from\n> <https://github.com/typeddjango/djangorestframework-stubs> with the goal of\n> removing the [`mypy`](https://github.com/python/mypy) plugin dependency so\n> that `mypy` can't [crash due to Django\n> config](https://github.com/typeddjango/django-stubs/issues/318), and that\n> non-`mypy` type checkers like\n> [`pyright`](https://github.com/microsoft/pyright) will work better with\n> Django Rest Framework.\n\n## install\n\n```bash\npip install djangorestframework-types\n```\n\n## related\n\n- <https://github.com/sbdchd/django-types>\n",
    'author': 'Steve Dignam',
    'author_email': 'steve@dignam.xyz',
    'url': 'https://github.com/sbdchd/djangorestframework-types',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
