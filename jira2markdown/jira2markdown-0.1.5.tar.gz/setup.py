# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jira2markdown', 'jira2markdown.markup']

package_data = \
{'': ['*']}

install_requires = \
['pyparsing>=2.4,<3.0']

setup_kwargs = {
    'name': 'jira2markdown',
    'version': '0.1.5',
    'description': 'Convert text from JIRA markup to Markdown using parsing expression grammars',
    'long_description': '# jira2markdown\n\n`jira2markdown` is a text converter from [JIRA markup](https://jira.atlassian.com/secure/WikiRendererHelpAction.jspa?section=all) to [YouTrack Markdown](https://www.jetbrains.com/help/youtrack/standalone/youtrack-markdown-syntax-issues.html) using parsing expression grammars. The Markdown implementation in YouTrack follows the [CommonMark specification](https://spec.commonmark.org/0.29/) with extensions. Thus, `jira2markdown` can be used to convert text to any Markdown syntax with minimal modifications.\n\n# Prerequisites\n\n- Python 3.6+\n\n# Installation\n\n```\npip install jira2markdown\n```\n\n# Usage\n\n```python\nfrom jira2markdown import convert\n\nconvert("Some *Jira text* formatting [example|https://example.com].")\n# >>> Some **Jira text** formatting [example](https://example.com).\n\n# To convert user mentions provide a mapping Jira internal account id to username \n# as a second argument to convert function\nconvert("[Winston Smith|~accountid:internal-id] woke up with the word \'Shakespeare\' on his lips", {\n    "internal-id": "winston",\n})\n# >>> @winston woke up with the word \'Shakespeare\' on his lips\n```\n',
    'author': 'Evgeniy Krysanov',
    'author_email': 'evgeniy.krysanov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/catcombo/jira2markdown',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
