# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sentry_msg', 'sentry_wrapper']

package_data = \
{'': ['*']}

install_requires = \
['sentry-sdk>=0.20.3,<0.21.0']

entry_points = \
{'console_scripts': ['sentry-msg = sentry_msg:execute',
                     'sentry-wrapper = sentry_wrapper:execute']}

setup_kwargs = {
    'name': 'sentry-wrapper',
    'version': '2.5.0',
    'description': 'Forward exceptions raised by a setuptools entrypoint to sentry',
    'long_description': "DESCRIPTION\n===========\n\nsentry-wrapper calls a setuptools entrypoint and sends exceptions to sentry. It\nis useful to log the exceptions of a correctly packaged but not sentry-capable\nprogram.\n\n\nUsage::\n\n    usage: sentry-wrapper [options] [-- entrypoint options]\n\n    positional arguments:\n      name                  Entry point name (eg. my-entrypoint)\n      dist                  Distribution name (eg. my-project==1.2.4, default:\n                            same value than name)\n      group                 Entry point group (default: console_scripts)\n\n    optional arguments:\n      -h, --help            show this help message and exit\n      --dsn SENTRY_DSN      Sentry DSN\n      -t timeout, --timeout timeout\n                            Timeout. After this value, TimeoutError is raised to\n                            Sentry.\n\n\nFor example, if the `setup.py` file of the package `mypackage` contains::\n\n    ...\n    name='my-package',\n    entry_points={\n        'console_scripts': [\n            'my-entrypoint = mypackage:main',\n        ],\n    },\n    ...\n\nCall `my-entrypoint` with::\n\n    sentry-wrapper --dsn SENTRY_DSN my-entrypoint my-package console_scripts\n\n\nINSTALLATION\n============\n\nTo install in a virtualenv::\n\n    $> virtualenv myenv\n    $> source myenv/bin/activate\n    $> pip install sentry-wrapper\n    $> pip install path/to/your/project\n    $> sentry-wrapper -h\n\n\nDEVELOP\n=======\n\nTo start hacking on sentry-wrapper using Docker::\n\n    $> make\n\nThen:\n\n- Visit http://localhost:9000 with the credentials test/test\n- Create a project and copy the DSN\n- Test sentry-wrapper against the test project of this repository::\n\n    sentry-wrapper --dsn [...] whatever_ok whatever console_scripts\n    sentry-wrapper --dsn [...] whatever_exception whatever console_scripts\n\nCONTRIBUTORS\n============\n\n* `Bastien Chatelard <https://github.com/bchatelard/>`_\n* `Julien Castets <https://github.com/brmzkw/>`_\n",
    'author': 'Julien Castets',
    'author_email': 'castets.j@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.infra.online.net/auth/account-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
