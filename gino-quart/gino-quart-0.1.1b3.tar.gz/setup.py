# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['gino_quart']
install_requires = \
['gino>=1.0.0rc2,<2.0.0', 'quart>=0.13,<0.15']

entry_points = \
{'gino.extensions': ['quart = gino_quart']}

setup_kwargs = {
    'name': 'gino-quart',
    'version': '0.1.1b3',
    'description': 'An extension for GINO to integrate with Quart',
    'long_description': "# gino-quart\n\n![test](https://github.com/python-gino/gino-quart/workflows/test/badge.svg)\n\n## Introduction\n\nAn extension for [GINO](https://github.com/python-gino/gino) to support [quart](https://gitlab.com/pgjones/quart) server.\n\n## Usage\n\nThe common usage looks like this:\n\n```python\nfrom quart import Quart\nfrom gino.ext.quart import Gino\n\napp = Quart()\ndb = Gino(app, **kwargs)\n```\n\n## Configuration\n\nGINO adds a `before_request`, `after_request` and `before_first_request` hook to the Quart app to setup and cleanup database according to\nthe configurations that passed in the `kwargs` parameter.\n\nThe config includes:\n\n| Name                         | Description                                                                                                       | Default     |\n| ---------------------------- | ----------------------------------------------------------------------------------------------------------------- | ----------- |\n| `driver`                     | the database driver                                                                                               | `asyncpg`   |\n| `host`                       | database server host                                                                                              | `localhost` |\n| `port`                       | database server port                                                                                              | `5432`      |\n| `user`                       | database server user                                                                                              | `postgres`  |\n| `password`                   | database server password                                                                                          | empty       |\n| `database`                   | database name                                                                                                     | `postgres`  |\n| `dsn`                        | a SQLAlchemy database URL to create the engine, its existence will replace all previous connect arguments.        | N/A         |\n| `retry_times`                | the retry times when database failed to connect                                                                   | `20`        |\n| `retry_interval`             | the interval in **seconds** between each time of retry                                                            | `5`         |\n| `pool_min_size`              | the initial number of connections of the db pool.                                                                 | N/A         |\n| `pool_max_size`              | the maximum number of connections in the db pool.                                                                 | N/A         |\n| `echo`                       | enable SQLAlchemy echo mode.                                                                                      | N/A         |\n| `ssl`                        | SSL context passed to `asyncpg.connect`                                                                           | `None`      |\n| `use_connection_for_request` | flag to set up lazy connection for requests.                                                                      | N/A         |\n| `retry_limit`                | the number of retries to connect to the database on start up.                                                     | 1           |\n| `retry_interval`             | seconds to wait between retries.                                                                                  | 1           |\n| `kwargs`                     | other parameters passed to the specified dialects, like `asyncpg`. Unrecognized parameters will cause exceptions. | N/A         |\n\n## Lazy Connection\n\nIf `use_connection_for_request` is set to be True, then a lazy connection is available\nat `request['connection']`. By default, a database connection is borrowed on the first\nquery, shared in the same execution context, and returned to the pool on response.\nIf you need to release the connection early in the middle to do some long-running tasks,\nyou can simply do this:\n\n```python\nawait request['connection'].release(permanent=False)\n```\n\n## Contributing\n\nYou're welcome to contribute to this project. It's really appreciated. Please [fork this project and create a pull request](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork) to the [dev branch](https://github.com/python-gino/gino-quart/tree/dev).\n\n- Dependency management is done via [poetry](https://python-poetry.org/)\n- Pull request for new features _must_ include the appropriate tests integrated in `tests/test_gino_quart.py`\n- You should format your code. Recommended is [black](https://black.readthedocs.io/en/stable/)\n\n## Attribution\n\nThe license holder of this extension is [Tony Wang](https://github.com/python-gino/gino-quart/blob/master/LICENSE).\n\nThis project is an extension to [GINO](https://github.com/python-gino/gino) and part of the [python-gino community](https://github.com/python-gino).\n",
    'author': 'Tony Wang',
    'author_email': 'wwwjfy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/python-gino/gino-quart',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
