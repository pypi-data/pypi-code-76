# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican', 'pelican.plugins.show_source']

package_data = \
{'': ['*']}

install_requires = \
['pelican>=4.5,<5.0']

extras_require = \
{'markdown': ['markdown>=3.2.2,<4.0.0']}

setup_kwargs = {
    'name': 'pelican-show-source',
    'version': '1.0.0',
    'description': 'Pelican plugin that adds a link to post source content',
    'long_description': 'Show Source: A Plugin for Pelican\n=================================\n\n[![Build Status](https://img.shields.io/github/workflow/status/pelican-plugins/show-source/build)](https://github.com/pelican-plugins/show-source/actions)\n[![PyPI Version](https://img.shields.io/pypi/v/pelican-show-source)](https://pypi.org/project/pelican-show-source/)\n![License](https://img.shields.io/pypi/l/pelican-show-source?color=blue)\n\nThis Pelican plugin allows you to place a link to your posts’ source content files in the same way that [Sphinx][] does. It works for both pages and articles.\n\nInstallation\n------------\n\nThis plugin can be installed via:\n\n    python -m pip install pelican-show-source\n\nFor more detailed plugin installation instructions, please refer to the [Pelican Plugin Documentation][].\n\nConfiguration\n-------------\n\nTo enable the plugin, ensure that you have `SHOW_SOURCE_ON_SIDEBAR = True` or `SHOW_SOURCE_IN_SECTION = True` in your settings file.\n\nMaking Source Available for Posts\n---------------------------------\n\nIn order to mark posts so that their source may be seen, use the following metadata fields (unless overridden) for reStructuredText documents:\n\n```rst\n:show_source: True\n```\n\nAlternatively, for Markdown syntax:\n\n```markdown\nShow_source: True\n```\n\nThe plugin will render your source document URL to a corresponding `article.show_source_url` (or `page.show_source_url`) attribute, which is then accessible in the site templates.\n\nShow Source in the Templates\n----------------------------\n\nTo get the “show source“ links to display in the article or page you will have to modify your theme, either as a sidebar display or at the foot of an article.\n\n### Article or Page Sidebar Display\n\nHow to get the source link to appear in the sidebar using the [pelican-bootstrap3][] theme:\n\n```html\n{% if SHOW_SOURCE_ON_SIDEBAR %}\n    {% if (article and article.show_source_url) or (page and page.show_source_url) %}\n        <li class="list-group-item"><h4><i class="fa fa-tags fa-file-text"></i><span class="icon-label">This Page</span></h4>\n            <ul class="list-group">\n                <li class="list-group-item">\n                    {% if article %}\n                    <a href="{{ SITEURL }}/{{ article.show_source_url }}">Show source</a>\n                    {% elif page %}\n                    <a href="{{ SITEURL }}/{{ page.show_source_url }}">Show source</a>\n                    {% endif %}\n                </li>\n            </ul>\n        </li>\n    {% endif %}\n{% endif %}\n```\n\n### Article Footer Display\n\nFollowing is some code (yes, [pelican-bootstrap3][] again) to enable a source link at the bottom of an article:\n\n```html\n{% if SHOW_SOURCE_IN_SECTION %}\n    {% if article and article.show_source_url %}\n    <section class="well" id="show-source">\n        <h4>This Page</h4>\n        <ul>\n            <a href="{{ SITEURL }}/{{ article.show_source_url }}">Show source</a>\n        </ul>\n    </section>\n    {% endif %}\n{% endif %}\n```\n\nOverriding Default Plugin Behaviour\n-----------------------------------\n\nThe default behaviour of the plugin is that revealing source is enabled on a case-by-case basis. This can be changed by the use of `SHOW_SOURCE_ALL_POSTS = True` in the settings file. This does mean that the plugin will publish all source documents no matter whether `show_source` is set in the metadata or not.\n\nUnless overridden, each document is saved as the article or page slug attribute with a `.txt` extension.\n\nSo for example, if your configuration had `ARTICLE_SAVE_AS` configured like so:\n\n```python\nARTICLE_SAVE_AS = "posts/{date:%Y}/{date:%m}/{slug}/index.html"\n```\n\n… your static HTML post and source text document will be like the following:\n\n```text\nposts/2016/10/welcome-to-my article/index.html\nposts/2016/10/welcome-to-my article/welcome-to-my article.txt\n```\n\nYou can add the `SHOW_SOURCE_FILENAME` variable in your settings file to override the source file name, so you could set the following:\n\n```python\nSHOW_SOURCE_FILENAME = "my_source_file.txt"\n```\n\nSo with the `ARTICLE_SAVE_AS` configured as above, the files would be saved\nthus:\n\n```text\nposts/2016/10/welcome-to-my article/index.html\nposts/2016/10/welcome-to-my article/my_source_file.txt\n```\n\nThis is the same behaviour for pages as well.\n\nContributing\n------------\n\nContributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].\n\nTo start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.\n\n[existing issues]: https://github.com/pelican-plugins/show-source/issues\n[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html\n\nLicense\n-------\n\nThis project is licensed under the AGPL-3.0 license.\n\n\n[Pelican Plugin Documentation]: https://docs.getpelican.com/en/latest/plugins.html\n[Sphinx]: https://www.sphinx-doc.org/\n[pelican-bootstrap3]: https://github.com/getpelican/pelican-themes/tree/master/pelican-bootstrap3\n',
    'author': 'Pelican Dev Team',
    'author_email': 'authors@getpelican.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pelican-plugins/show-source',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
