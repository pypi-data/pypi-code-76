# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['supervisor_react']

package_data = \
{'': ['*'],
 'supervisor_react': ['build/*',
                      'build/static/css/*',
                      'build/static/js/*',
                      'build/static/media/*']}

install_requires = \
['aiofiles', 'httpx', 'starlette', 'uvicorn']

entry_points = \
{'console_scripts': ['supervisor-react = supervisor_react:main']}

setup_kwargs = {
    'name': 'supervisor-react',
    'version': '0.1.8',
    'description': 'A web interface for supervisor',
    'long_description': 'supervisor-react\n================\n\nA web interface for supervisor made with React.\n\n```\nusage: supervisor-react [-h] [-d] [-p PORT] [-s SUPERVISOR] [-v]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -d, --debug\n  -p PORT, --port PORT\n  -s SUPERVISOR, --supervisor SUPERVISOR\n  -v, --verbose\n```\n',
    'author': 'Cyril Jouve',
    'author_email': 'jv.cyril@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jouve/supervisor-react',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
