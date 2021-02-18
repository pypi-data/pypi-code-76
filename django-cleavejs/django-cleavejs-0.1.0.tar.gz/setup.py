# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dj_cleavejs']

package_data = \
{'': ['*'], 'dj_cleavejs': ['static/*']}

install_requires = \
['Django>2.1,<4.0']

setup_kwargs = {
    'name': 'django-cleavejs',
    'version': '0.1.0',
    'description': 'Cleave.js integration for Django forms',
    'long_description': 'Cleave.js integration for Django forms\n======================================\n\nThis re-usable app helps integrating `Cleave.js`_ into Django projects.\nCleave.js is a JavaScript library that can "help you format input text\ncontent automatically".\n\n`django-cleavejs`_ eases integration into Django. It wraps `Cleave.js`_\'s\noptions object into a form widget class, which takes care of transporting\nthe options to JavaScript and initialising `Cleave.js`_ for each such\ninput field.\n\n\nInstallation\n------------\n\nTo add `django-cleavejs`_ to a project, first add it as dependency to your\nproject, e.g. using `poetry`_::\n\n  $ poetry add django-cleavejs\n\nThen, add it to your `INSTALLED_APPS` setting to make its static files\navailable::\n\n  INSTALLED_APPS = [\n      ...\n      "dj_cleavejs.apps.DjCleaveJSConfig",\n      ...\n  ]\n\nYou need to make `Cleave.js`_ itself available by some means. You can\ndownload it manually, or use your favourite asset management library. For\ninstance, you could use `django-yarnpkg`_ to depend on the `cleave.js`\nYarn package::\n\n  YARN_INSTALLED_APPS = [\n    "cleave.js",\n  ]\n  NODE_MODULES_ROOT = os.path.join(BASE_DIR, "node_modules")\n  STATICFILES_FINDERS += ["django_yarnpkg.finders.NodeModulesFinder"]\n\nYou can then either include it in your template yourself, or make\n`django-cleavejs`_ add it to its form media by configuring the URL or\npath in your settings::\n\n  CLEAVE_JS = "cleave.js/dist/cleave.min.js"\n\nThe above example uses the path below `STATIC_ROOT` where `django-yarnpkg`_\nwould put the package, but you can of course use any URL or path you want\ndepending on how you want to make `Cleave.js`_ available to the browser.\n\nUsage\n-----\n\nOnce available, you can create a form as normal and use the widget\non any `CharField`::\n\n  from django.forms import CharField, Form\n\n  from dj_cleavejs import CleaveWidget\n\n\n  class TestForm(Form):\n      windows_xp_serial = CharField(widget=CleaveWidget(blocks=[5, 5, 5, 5, 5],\n                              delimiter="-"))\n\nIn your template, make sure to include the form media of your form somewhere\n**after** the form.\n\nThe `CleaveWidget` supports all options `Cleave.js`_ supports, as described\nin its `options documentation`_. In the future, `django-cleavejs`_ will also\nprovide shortcuts.\n\nExample\n-------\n\nThe source distribution as well as the `Git repository`_ contain a full example\napplication that serves a test form unter `/test.html`.\n\nIt is reduced to a minimal working example for the reader\'s convenience.\n\n.. _django-cleavejs: https://edugit.org/AlekSIS/libs/django-cleavejs\n.. _poetry: https://python-poetry.org/\n.. _Cleave.js: https://nosir.github.io/cleave.js/\n.. _django-yarnpkg: https://edugit.org/AlekSIS/libs/django-yarnpkg\n.. _options documentation: https://github.com/nosir/cleave.js/blob/master/doc/options.md\n.. _Git repository: https://edugit.org/AlekSIS/libs/django-cleavejs\n',
    'author': 'Dominik George',
    'author_email': 'dominik.george@teckids.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://edugit.org/AlekSIS/libs/django-cleavejs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
