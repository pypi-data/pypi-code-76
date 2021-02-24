# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['djankiserv',
 'djankiserv.api',
 'djankiserv.assets.jsonfiles',
 'djankiserv.assets.sql.sqlite3',
 'djankiserv.migrations',
 'djankiserv.sync',
 'djankiserv.unki']

package_data = \
{'': ['*']}

install_requires = \
['django-k8s>=0.2.9,<0.3.0',
 'django>=3.1,<4.0',
 'djangorestframework-simplejwt>=4.4.0,<5.0.0',
 'djangorestframework>=3.11.1,<4.0.0',
 'gunicorn>=20.0.4,<21.0.0']

extras_require = \
{'mysql': ['mysqlclient>=2.0.1,<3.0.0'],
 'pgsql': ['psycopg2-binary>=2.8.6,<3.0.0']}

setup_kwargs = {
    'name': 'djankiserv',
    'version': '0.0.9',
    'description': 'Django-based synchronisation and API server for Anki',
    'long_description': '# djankiserv\n\n`djankiserv` is an open source Django-based implementation of a synchronisation server for Anki 2.1+. It includes a user manager (the native Django user system).\n\n[Installation](doc/Installation.md) -\xa0[Connecting Anki to the sync server](doc/ConnectingAnki.md) - [Development](doc/Development.md) - [Contributing](doc/CONTRIBUTING.md)\n\n## About this implementation\n\nThis implementation was initially developed in order to support the spaced repetition functionality for [`Transcrobes`](https://transcrob.es), an open source language learning platform/ecosystem.\n\nAny requests or functionality that don\'t interfere with using this project for that will definitely be entertained. Ideally the server would do everything that Ankiweb does, and much more. PRs are obviously always welcome!\n\n### Technical differences\n\nUnlike the other popular open source Anki synchronisation server [`anki-sync-server`](https://github.com/ankicommunity/anki-sync-server), `djankiserv` stores the user data in a "proper" RDBMS. There are two \'database connections\' that can be set - those for the \'system\' (sessions, users, etc.) and those for user data. The \'system\' stuff is just plain old Django, so any supported database can be used. The user data part currently uses either `postgresql` schemas or `mysql` databases, and currently only supports those two, though supporting other RDBMSes will definitely be considered later. `sqlite3` is an embedded database and works great for that. It is not appropriate for use in modern web applications in the opinion of the maintainer, so will never be supported by `djankiserv`.\n\nThere is a basic API for getting certain, per-user collection-related information (decks, deck configuration, models, tags) and also `notes` for a given user. It may evolve to include other functions, statistics and even doing cards, though the focus is currently on getting and maintaining proper synchronisation as well as the basic API for `notes`.\n\n### Limitations\n\nThis is alpha software with some occasional data loss bugs. It works, sorta, if you hold it right. If it kills your kittens then you were forewarned!\n\nCurrent known limitations (bugs!):\n\n- it doesn\'t support abort and if it crashes in the middle of a sync then the server will have a corrupt view of the database. You should force an upload sync on next synchronisation if this ever happens!\n- The v2 scheduler is not supported, and it is unclear how difficult this might be to implement.\n',
    'author': 'Anton Melser',
    'author_email': 'anton@melser.org',
    'maintainer': 'Anton Melser',
    'maintainer_email': 'anton@melser.org',
    'url': 'https://github.com/ankicommunity/djankiserv',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
