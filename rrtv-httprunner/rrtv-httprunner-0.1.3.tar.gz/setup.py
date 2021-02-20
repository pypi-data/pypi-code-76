# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rrtv_httprunner',
 'rrtv_httprunner.app',
 'rrtv_httprunner.app.routers',
 'rrtv_httprunner.builtin',
 'rrtv_httprunner.ext',
 'rrtv_httprunner.ext.har2case',
 'rrtv_httprunner.ext.locust',
 'rrtv_httprunner.ext.uploader']

package_data = \
{'': ['*']}

install_requires = \
['black>=19.10b0,<20.0',
 'jinja2>=2.10.3,<3.0.0',
 'jmespath>=0.9.5,<0.10.0',
 'loguru>=0.4.1,<0.5.0',
 'pydantic>=1.4,<2.0',
 'pytest-html>=2.1.1,<3.0.0',
 'pytest>=5.4.2,<6.0.0',
 'pyyaml>=5.1.2,<6.0.0',
 'requests>=2.22.0,<3.0.0',
 'sentry-sdk>=0.14.4,<0.15.0']

extras_require = \
{'allure': ['allure-pytest>=2.8.16,<3.0.0'],
 'locust': ['locust>=1.0.3,<2.0.0'],
 'upload': ['requests-toolbelt>=0.9.1,<0.10.0', 'filetype>=1.0.7,<2.0.0']}

entry_points = \
{'console_scripts': ['har2case = httprunner.cli:main_har2case_alias',
                     'hmake = httprunner.cli:main_make_alias',
                     'hrun = httprunner.cli:main_hrun_alias',
                     'httprunner = httprunner.cli:main',
                     'locusts = httprunner.ext.locust:main_locusts']}

setup_kwargs = {
    'name': 'rrtv-httprunner',
    'version': '0.1.3',
    'description': 'One-stop solution for HTTP(S) testing.',
    'long_description': None,
    'author': 'chenfanghang',
    'author_email': 'chenfanghang@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
