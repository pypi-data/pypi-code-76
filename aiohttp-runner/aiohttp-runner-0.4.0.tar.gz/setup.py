# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiohttp_runner']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3,<4', 'async-exit-stack>=1,<2']

setup_kwargs = {
    'name': 'aiohttp-runner',
    'version': '0.4.0',
    'description': 'Wraps aiohttp or gunicorn server for aiohttp application.',
    'long_description': "Usage\n=====\n\n```python\nimport aiohttp.web\nfrom async_generator import asynccontextmanager\nfrom aiohttp_runner import (\n    SimpleHttpRunner, GunicornHttpRunner, HttpWorkerContext, HttpRequest, HttpResponse,\n    create_http_app,\n)\n\n\n@asynccontextmanager\nasync def app_factory(_context: HttpWorkerContext):\n    yield create_http_app(routes=[\n        ('GET', '/', http_handler),\n    ])\n\n\nasync def http_handler(_req: HttpRequest) -> HttpResponse:\n    return aiohttp.web.Response(status=204)\n\n\nSimpleHttpRunner(bind='0.0.0.0:8080').run(app_factory)\n# OR\nGunicornHttpRunner(bind='0.0.0.0:8080', workers=3).run(app_factory)\n```\n",
    'author': 'xppt',
    'author_email': '21246102+xppt@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
