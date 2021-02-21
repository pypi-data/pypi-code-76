# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['whats_that_code', 'whats_that_code.commands']

package_data = \
{'': ['*']}

install_requires = \
['defusedxml', 'pygments', 'pyrankvote']

setup_kwargs = {
    'name': 'whats-that-code',
    'version': '0.1.11',
    'description': 'Guess programming language from a string or file.',
    'long_description': '# whats_that_code\nThis is a programming language detection library.\n\nIt will detect programming language of source in pure python from an ensemble of classifiers.\nUse this when a quick and dirty first approximation is good enough.\nwhats_that_code can currently identify 60%+ of samples without knowing the extension or tag.\n\nI created this because I wanted\n- a pure python programming language detector\n- no machine learning dependencies\n\nTested on python 3.6 through 3.9.\n\n## Usage\n```\n> code = "def yo():\\n   print(\'hello\')"\n> guess_language_all_methods(code, file_name="yo.py")\n["python"]\n```\n\n## How it Works\n1) Inspects file extension if available.\n2) Inspects shebang\n3) Looks for keywords\n4) Counts regexes for common patterns\n5) Attemps to parse python, json, yaml\n6) Inspects tags if available.\n\nEach is imperfect and can error. The classifier then combines the results of each using a voting algorithm\n\nThis works best if you only use it for fallback, e.g. classifying code that can\'t already be classified by extension or tag,\nor when tag is ambiguous.\n\nIt was a tool that outgrew being a part of [so_pip](https://github.com/matthewdeanmartin/so_pip) a StackOverflow code\nextraction tool I wrote.\n\n## Docs\n- [TODO](https://github.com/matthewdeanmartin/whats_that_code/tree/main/docs/TODO.md)\n- [LICENSE](https://github.com/matthewdeanmartin/whats_that_code/tree/main/LICENSE)\n- [Prior Art](https://github.com/matthewdeanmartin/whats_that_code/tree/main/docs/prior_art.md) Every similar project/tool, including defunct\n- [ChangeLog](https://github.com/matthewdeanmartin/whats_that_code/tree/main/docs/CHANGES.md)\n\n## Notable Similar Tools\n- [Guesslang](https://pypi.org/project/guesslang/) - python and tensorflow driven solution. Reasonable results but\nslow startup and not pure python.\n- [pygments](https://pygments.org/docs/api/#pygments.lexers.guess_lexer) pure python, but sometimes lousy identification\nrates.\n',
    'author': 'Matthew Martin',
    'author_email': 'matthewdeanmartin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/matthewdeanmartin/whats_that_code',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
