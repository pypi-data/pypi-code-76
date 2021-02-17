# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican', 'pelican.plugins.tag_cloud']

package_data = \
{'': ['*'], 'pelican.plugins.tag_cloud': ['test_data/*']}

install_requires = \
['pelican>=4.5,<5.0']

extras_require = \
{'markdown': ['markdown>=3.2.2,<4.0.0']}

setup_kwargs = {
    'name': 'pelican-tag-cloud',
    'version': '1.0.0',
    'description': 'Pelican plugin that generates a tag cloud from post tags',
    'long_description': 'Tag Cloud: A Plugin for Pelican\n===============================\n\n[![Build Status](https://img.shields.io/github/workflow/status/pelican-plugins/tag-cloud/build)](https://github.com/pelican-plugins/tag-cloud/actions)\n[![PyPI Version](https://img.shields.io/pypi/v/pelican-tag-cloud)](https://pypi.org/project/pelican-tag-cloud/)\n![License](https://img.shields.io/pypi/l/pelican-tag-cloud?color=blue)\n\nThis Pelican plugin generates a tag cloud from post tags.\n\nInstallation\n------------\n\nThis plugin can be installed via:\n\n    python -m pip install pelican-tag-cloud\n\nFor more detailed plugin installation instructions, please refer to the [Pelican Plugin Documentation](https://docs.getpelican.com/en/latest/plugins.html).\n\nIn order to use to use this plugin, you must edit your theme’s base template and style-sheet. You should change **base.html** to apply formats (and sizes) defined in **style.css**, as specified in _Settings_ below.\n\nSettings\n--------\n\n| Settings and their default values  |                   What does it do?                    |\n| ---------------------------------- | ----------------------------------------------------- |\n| `TAG_CLOUD_STEPS = 4`              |  Count of different font sizes in the tag cloud       |\n| `TAG_CLOUD_MAX_ITEMS = 100`        |  Maximum number of tags in the cloud                  |\n| `TAG_CLOUD_SORTING = "random"`     |  Tag cloud ordering scheme. Valid values: random, alphabetically, alphabetically-rev, size, and size-rev |\n| `TAG_CLOUD_BADGE = True`           |  Optional setting: turn on **badges**, displaying the number of articles using each tag |\n\nUsage\n-----\n\nThe default theme does not include a tag cloud, but it is fairly easy to add one:\n\n```jinja2\n<ul class="tagcloud">\n    {% for tag in tag_cloud %}\n        <li class="tag-{{ tag.1 }}">\n            <a href="{{ SITEURL }}/{{ tag.0.url }}">\n            {{ tag.0 }}\n                {% if TAG_CLOUD_BADGE %}\n                    <span class="badge">{{ tag.2 }}</span>\n                {% endif %}\n            </a>\n        </li>\n    {% endfor %}\n</ul>\n```\n\nYou should then also define CSS styles with appropriate classes (tag-1 to tag-N, where N matches `TAG_CLOUD_STEPS`), tag-1 being the most frequent, and define a `ul.tagcloud` class with appropriate list-style to create the cloud. You should copy+paste this **badge** CSS rule `ul.tagcloud .list-group-item <span>.badge` if you are using the `TAG_CLOUD_BADGE` setting. (This rule, potentially long, is suggested to avoid conflicts with CSS frameworks such as Twitter Bootstrap.)\n\nFor example:\n\n```css\nul.tagcloud {\n    list-style: none;\n    padding: 0;\n}\n\nul.tagcloud li {\n    display: inline-block;\n}\n\nli.tag-1 {\n    font-size: 150%;\n}\n\nli.tag-2 {\n    font-size: 120%;\n}\n\n/* ... add li.tag-3 etc, as much as needed */\n\nul.tagcloud .list-group-item span.badge {\n    background-color: grey;\n    color: white;\n}\n```\n\nBy default, the tags in the cloud are sorted randomly, but if you prefer to have them sorted alphabetically, use `alphabetically` (ascending) and `alphabetically-rev` (descending). Also, it is possible to sort the tags by frequency (number of articles with this specific tag) using the values `size` (ascending) and `size-rev` (descending).\n\nContributing\n------------\n\nContributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].\n\nTo start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.\n\n[existing issues]: https://github.com/pelican-plugins/tag-cloud/issues\n[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html\n\nLicense\n-------\n\nThis project is licensed under the AGPL-3.0 license.\n',
    'author': 'Pelican Dev Team',
    'author_email': 'authors@getpelican.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pelican-plugins/tag-cloud',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
