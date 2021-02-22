# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cli',
 'conf',
 'core',
 'core.lib',
 'core.nodes',
 'core.outputs',
 'core.renders']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0',
 'configparser>=5.0.1,<6.0.0',
 'environ-config>=20.1.0,<21.0.0',
 'pretty-errors>=1.2.19,<2.0.0',
 'pydash>=4.9.1,<5.0.0',
 'python-frontmatter>=0.5.0,<0.6.0',
 'shellingham>=1.4.0,<2.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['sigla = src.cli.cli:app']}

setup_kwargs = {
    'name': 'sigla',
    'version': '0.0.54',
    'description': 'Yet another code generator',
    'long_description': None,
    'author': 'mg santos',
    'author_email': 'mauro.goncalo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
