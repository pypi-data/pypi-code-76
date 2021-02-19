# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['symphony',
 'symphony.bdk',
 'symphony.bdk.core',
 'symphony.bdk.core.auth',
 'symphony.bdk.core.client',
 'symphony.bdk.core.config',
 'symphony.bdk.core.config.model',
 'symphony.bdk.core.service',
 'symphony.bdk.core.service.connection',
 'symphony.bdk.core.service.connection.model',
 'symphony.bdk.core.service.datafeed',
 'symphony.bdk.core.service.message',
 'symphony.bdk.core.service.stream',
 'symphony.bdk.core.service.user',
 'symphony.bdk.core.service.user.model',
 'symphony.bdk.gen',
 'symphony.bdk.gen.agent_api',
 'symphony.bdk.gen.agent_model',
 'symphony.bdk.gen.auth_api',
 'symphony.bdk.gen.auth_model',
 'symphony.bdk.gen.login_api',
 'symphony.bdk.gen.login_model',
 'symphony.bdk.gen.pod_api',
 'symphony.bdk.gen.pod_model']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.3,<4.0.0',
 'nulltype>=2.3.1,<3.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'python-jose>=3.2.0,<4.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'urllib3>=1.26.2,<2.0.0']

setup_kwargs = {
    'name': 'sym-api-client-python',
    'version': '2.0b0',
    'description': 'Symphony Bot Development Kit for Python',
    'long_description': '# symphony-api-client-python\n\nThis is the Symphony BDK for Python to help developing bots and interact with the [Symphony REST APIs](https://developers.symphony.com/restapi/reference).\n\nLegacy Python BDK is located in [legacy](./legacy) folder.\n\n## How to build\n\nWe use [poetry](https://python-poetry.org/) in order to manage dependencies, build, run tests and publish.\nTo install poetry, follow instructions [here](https://python-poetry.org/docs/#installation).\n\nOn the first time, run `poetry install`. Then run `poetry build` to build the sdist and wheel packages.\nTo run the tests, use `poetry run pytest`.\n',
    'author': 'Symphony Platform Solutions',
    'author_email': 'platformsolutions@symphony.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
