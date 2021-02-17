# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican', 'pelican.plugins.linkclass']

package_data = \
{'': ['*']}

install_requires = \
['pelican>=4.5,<5.0']

extras_require = \
{'markdown': ['markdown>=3.2.2,<4.0.0']}

setup_kwargs = {
    'name': 'pelican-linkclass',
    'version': '2.0.0',
    'description': "Pelican plugin to set anchor tag's class attribute to differentiate between internal and external links",
    'long_description': "Link Class: A Plugin for Pelican\n================================\n\n[![Build Status](https://img.shields.io/github/workflow/status/pelican-plugins/linkclass/build)](https://github.com/pelican-plugins/linkclass/actions)\n[![PyPI Version](https://img.shields.io/pypi/v/pelican-linkclass)](https://pypi.org/project/pelican-linkclass/)\n![License](https://img.shields.io/pypi/l/pelican-linkclass?color=blue)\n\nThis Pelican plugin allows you to set the class attribute of `<a>` elements\n(generated in Markdown by `[ext](link)`) according to whether the link is\nexternal (i.e., starts with `http://` or `https://`) or internal to the\nPelican-generated site.\n\nFor now, this plugin only works with Markdown. It has been tested with version\n3.0+ of the Python-Markdown module and may not work with previous versions.\n\nInstallation\n------------\n\nThis plugin [is available as a package](https://pypi.org/project/pelican-linkclass/)\nat PyPI and can be installed via:\n\n```\npython -m pip install pelican-linkclass\n```\n\nConfiguration\n-------------\n\nIn order to avoid clashes with already-defined classes in the user CSS\nstyle sheets, it is possible to specify the name of the classes that will\nbe used. They can be specified in the Pelican setting file with the\n`LINKCLASS` variable, which must be defined as a list of tuples, like this:\n\n```python\n'LINKCLASS' = (('EXTERNAL_CLASS', 'name-of-the-class-for-external-links')\n                'INTERNAL_CLASS', 'name-of-the-class-for-internal-links'))\n```\n\nThe default values for `EXTERNAL_CLASS` and `INTERNAL_CLASS` are,\nrespectively, `'external'` and `'internal'`.\n\nStyling Hyperlinks\n------------------\n\nOne of the possible uses of this plugins is for styling. Suppose that we\nhave the following Markdown content in your article:\n\n```markdown\nThis is an [internal](internal) link and this is an\n[external](http://external.com) link.\n```\n\nIf the default configuration variable values are used, then one possible\nCSS setting could be:\n\n```css\na.external:before {\n    content: url('../images/external-link.png');\n    margin-right: 0.2em;\n}\n```\n\n(The file `external-link.png` is also distributed with this plugin. To use it,\ncopy it to the appropriate place in your web site source tree, for instance\nin `theme/static/images/`.)\n\nThen, the result will look like the following:\n\n![figure](https://github.com/rlaboiss/pelican-linkclass/raw/master/linkclass-example.png)\n\nNote that this plugin also works with reference-style links, as in the\nfollowing example:\n\n```markdown\nThis is an [internal][internal] link and this is an\n[external][external] link.\n\n [internal]: internal\n [external]: http://external.com\n```\n\nContributing\n------------\n\nContributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].\n\nTo start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.\n\n[existing issues]: https://github.com/pelican-plugins/linkclass/issues\n[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html\n\nAcknowledgments\n---------------\n\nMany thanks to [Yuliya Bagriy](https://github.com/aviskase) for\nsetting up the package for [PyPI](https://pypi.org/), to [Lucas\nCimon](https://github.com/Lucas-C) for fixing the issues with\n[pytest](https://pytest.org/), and to [Justin\nMayer](https://github.com/justinmayer) for helping with migration of\nthis plugin under the Pelican Plugins organization.\n\nAuthor\n------\n\nCopyright (C) 2015, 2017, 2019, 2021  Rafael Laboissière (<rafael@laboissiere.net>)\n\nReleased under the GNU Affero Public License, version 3 or later. No warranties.\n",
    'author': 'Rafael Laboissière',
    'author_email': 'rafael@laboissiere.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pelican-plugins/linkclass',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
