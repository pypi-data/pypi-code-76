# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sheraf',
 'sheraf.attributes',
 'sheraf.health',
 'sheraf.models',
 'sheraf.tools',
 'sheraf.types']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'rich>=9.10.0,<10.0.0', 'zodb>=5', 'zodburi']

extras_require = \
{'all': ['zeo', 'psycopg2', 'psycopg2cffi', 'relstorage'],
 'doc': ['recommonmark', 'sphinx', 'sphinx-rtd-theme', 'sphinx-issues'],
 'relstorage_pg': ['psycopg2', 'psycopg2cffi', 'relstorage'],
 'zeo': ['zeo']}

entry_points = \
{'console_scripts': ['sheraf = sheraf.cli:cli']}

setup_kwargs = {
    'name': 'sheraf',
    'version': '0.4.0',
    'description': 'Versatile ZODB abstraction layer',
    'long_description': '# A versatile ZODB abstraction layer\n\nsheraf is an overlay over ZODB. It provides a high level interface to save and read your data.\n\n## Installation\n\nsheraf is compatible with Python 3.6+\n\n    poetry add sheraf\n    # or\n    pip install sheraf\n\nIf you need pytest fixtures for your project check out [pytest-sheraf](https://gitlab.com/yaal/pytest-sheraf). There are also [sheraf fixtures for unittest](https://gitlab.com/yaal/unittest-sheraf).\n\n    pip install pytest-sheraf\n\nThe documentation is [hosted here](https://sheraf.readthedocs.io/en/latest/).\n\n## Contributing\n\nBug reports and pull requests are highly encouraged!\n\n - Test some code : `poetry run pytest` and `poetry run tox`\n - Format code :\xa0`black`\n - Generate documentation : `poetry run tox -e doc`\n\n## Documentation\n\n    poetry run tox -e doc\n    open build/sphinx/html/index.html\n\n## Development installation\n\nsheraf use poetry as its main build tool. Do not hesitate to check [the documentation](https://python-poetry.org/docs/).\n\n    poetry install --extras all\n',
    'author': 'Yaal team',
    'author_email': 'contact@yaal.fr',
    'maintainer': 'Éloi Rivard',
    'maintainer_email': 'eloi@yaal.fr',
    'url': 'https://sheraf.readthedocs.io/en/latest/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
