# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioworkers_pg']

package_data = \
{'': ['*']}

install_requires = \
['aioworkers>=0.15', 'asyncpg<=0.21.0', 'asyncpgsa<0.27.0']

setup_kwargs = {
    'name': 'aioworkers-pg',
    'version': '0.2.1',
    'description': 'Module for working with PostgreSQL via asyncpg',
    'long_description': "# aioworkers-pg\n\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aioworkers-pg)\n![PyPI](https://img.shields.io/pypi/v/aioworkers-pg)\n\nAsyncpg plugin for `aioworkers`.\n\n\n## Usage\n\nAdd this to aioworkers config.yaml:\n\n```yaml\ndb:\n  cls: aioworkers_pg.base.Connector\n  dsn: postgresql:///test\n```\n\nYou can get access to postgres anywhere via context:\n\n```python\nawait context.db.execute('CREATE TABLE users(id serial PRIMARY KEY, name text)')\nawait context.db.execute(users.insert().values(name='Bob'))\n```\n\n\n## Storage\n\n```yaml\nstorage:\n  cls: aioworkers_pg.storage.RoStorage\n  dsn: postgresql:///test\n  table: mytable  # optional instead custom sql\n  key: id\n  get: SELECT * FROM mytable WHERE id = :id  # optional custom sql\n  format: dict  # or row\n```\n\n## Development\n\nInstall dev requirements:\n\n```shell\npoetry install\n```\n\nRun postgres:\n\n```shell\ndocker run --rm -p 5432:5432 --name postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=test -d postgres\n```\n\nRun tests:\n\n```shell\npytest\n```\n",
    'author': 'Alexander Bogushov',
    'author_email': 'abogushov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aioworkers/aioworkers-pg',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
