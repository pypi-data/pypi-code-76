# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_unicorn',
 'django_unicorn.components',
 'django_unicorn.management.commands',
 'django_unicorn.templatetags']

package_data = \
{'': ['*'],
 'django_unicorn': ['static/js/*',
                    'static/js/morphdom/2.6.1/*',
                    'static/svg/*',
                    'templates/unicorn/*']}

install_requires = \
['beautifulsoup4>=4.8.0',
 'cachetools>=4.1.1,<5.0.0',
 'django>=3.0.0',
 'orjson>=3.2.1,<4.0.0',
 'shortuuid>=1.0.1,<2.0.0',
 'wrapt>=1.12.1,<2.0.0']

setup_kwargs = {
    'name': 'django-unicorn',
    'version': '0.21.0',
    'description': 'A magical full-stack framework for Django.',
    'long_description': '<p align="center">\n  <a href="https://www.django-unicorn.com/"><img src="https://www.django-unicorn.com/static/img/unicorn.svg" alt="django-unicorn logo" height="80"/></a>\n</p>\n<h1 align="center">Unicorn</h1>\n<p align="center">The magical full-stack framework for Django ✨</p>\n\n![PyPI](https://img.shields.io/pypi/v/django-unicorn?color=blue&style=flat-square)\n\n<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->\n[![All Contributors](https://img.shields.io/badge/all_contributors-6-orange.svg?style=flat-square)](#contributors-)\n<!-- ALL-CONTRIBUTORS-BADGE:END -->\n\n[Unicorn](https://www.django-unicorn.com) is a reactive component framework that progressively enhances a normal Django view, makes AJAX calls in the background, and dynamically updates the DOM. It seamlessly extends Django past its server-side framework roots without giving up all of its niceties or re-building your website.\n\n## :zap: How to use\n\n1. [Install](https://www.django-unicorn.com/docs/installation/) `Unicorn`\n1. [Create](https://www.django-unicorn.com/docs/components/) a component\n1. Load the `Unicorn` templatetag with `{% load unicorn %}` and add the component to your template with `{% unicorn \'component-name\' %}`\n1. :tada:\n\n## :book: More details\n\n- [Changelog](https://www.django-unicorn.com/docs/changelog/)\n- [Docs](https://www.django-unicorn.com/docs/)\n- [Screencasts](https://www.django-unicorn.com/screencasts/installation)\n- [Examples](https://www.django-unicorn.com/examples/todo)\n\n## :clap: Contributors\n\nThanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):\n\n<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->\n<!-- prettier-ignore-start -->\n<!-- markdownlint-disable -->\n<table>\n  <tr>\n    <td align="center"><a href="https://adamghill.com"><img src="https://avatars0.githubusercontent.com/u/317045?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Adam Hill</b></sub></a><br /><a href="https://github.com/adamghill/django-unicorn/commits?author=adamghill" title="Code">💻</a> <a href="https://github.com/adamghill/django-unicorn/commits?author=adamghill" title="Tests">⚠️</a></td>\n    <td align="center"><a href="https://python3.ninja"><img src="https://avatars1.githubusercontent.com/u/44167?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Andres Vargas</b></sub></a><br /><a href="https://github.com/adamghill/django-unicorn/commits?author=zodman" title="Code">💻</a></td>\n    <td align="center"><a href="http://iskra.ml"><img src="https://avatars3.githubusercontent.com/u/6555851?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Eddy Ernesto del Valle Pino</b></sub></a><br /><a href="https://github.com/adamghill/django-unicorn/commits?author=edelvalle" title="Code">💻</a></td>\n    <td align="center"><a href="https://www.linkedin.com/in/yaser-al-najjar-429b9096/"><img src="https://avatars3.githubusercontent.com/u/10493809?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Yaser Al-Najjar</b></sub></a><br /><a href="https://github.com/adamghill/django-unicorn/commits?author=yaseralnajjar" title="Code">💻</a></td>\n    <td align="center"><a href="https://github.com/sbidy"><img src="https://avatars.githubusercontent.com/u/1077364?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Stephan Traub</b></sub></a><br /><a href="https://github.com/adamghill/django-unicorn/commits?author=sbidy" title="Tests">⚠️</a></td>\n    <td align="center"><a href="https://github.com/frbor"><img src="https://avatars.githubusercontent.com/u/2320183?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Fredrik Borg</b></sub></a><br /><a href="https://github.com/adamghill/django-unicorn/commits?author=frbor" title="Code">💻</a> <a href="https://github.com/adamghill/django-unicorn/commits?author=frbor" title="Tests">⚠️</a></td>\n  </tr>\n</table>\n\n<!-- markdownlint-restore -->\n<!-- prettier-ignore-end -->\n\n<!-- ALL-CONTRIBUTORS-LIST:END -->\n\nThis project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!\n',
    'author': 'Adam Hill',
    'author_email': 'unicorn@adamghill.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.django-unicorn.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
