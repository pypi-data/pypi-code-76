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
    'version': '0.1.6',
    'description': 'Convert text from JIRA markup to Markdown using parsing expression grammars',
    'long_description': '# jira2markdown\n\n`jira2markdown` is a text converter from [JIRA markup](https://jira.atlassian.com/secure/WikiRendererHelpAction.jspa?section=all) to [YouTrack Markdown](https://www.jetbrains.com/help/youtrack/standalone/youtrack-markdown-syntax-issues.html) using parsing expression grammars. The Markdown implementation in YouTrack follows the [CommonMark specification](https://spec.commonmark.org/0.29/) with extensions. Thus, `jira2markdown` can be used to convert text to any Markdown syntax with minimal modifications.\n\n# Prerequisites\n\n- Python 3.6+\n\n# Installation\n\n```\npip install jira2markdown\n```\n\n# Usage\n\n```python\nfrom jira2markdown import convert\n\nconvert("Some *Jira text* formatting [example|https://example.com].")\n# >>> Some **Jira text** formatting [example](https://example.com).\n\n# To convert user mentions provide a mapping Jira internal account id to username \n# as a second argument to convert function\nconvert("[Winston Smith|~accountid:internal-id] woke up with the word \'Shakespeare\' on his lips", {\n    "internal-id": "winston",\n})\n# >>> @winston woke up with the word \'Shakespeare\' on his lips\n```\n\n# Conversion tables\n\n## Headings\n\n| Jira | Markdown |\n|------|----------|\n|`h1. Biggest heading`|`# Biggest heading`|\n|`h2. Bigger heading`|`## Bigger heading`|\n|`h3. Big heading`|`### Big heading`|\n|`h4. Normal heading`|`#### Normal heading`|\n|`h5. Small heading`|`##### Small heading`|\n|`h6. Smallest heading`|`###### Smallest heading`|\n\n## Text Effects\n\n| Jira | Markdown |\n|------|----------|\n|`*strong*`|`**strong**`|\n|`_emphasis_`|Not converted (the same syntax)|\n|`??citation??`|Not converted|\n|`-deleted-`|`~~deleted~~`|\n|`+inserted+`|`inserted`|\n|`^superscript^`|Not converted|\n|`~subscript~`|Not converted|\n|`{{monospaced}}`|`` `monospaced` ``|\n|`bq. Some block quoted text`|`> Some block quoted text`|\n|`{quote}Content to be quoted{quote}`|`> Content to be quoted`|\n|`{color:red}red text!{color}`|`<font color="red">red text!<font>`|\n\n## Text Breaks\n\n| Jira | Markdown |\n|------|----------|\n|`\\\\`|Line break|\n|`---`|`—`|\n|`--`|`–`|\n\n## Links\n\n| Jira | Markdown |\n|------|----------|\n|`[#anchor]`|Not converted|\n|`[^attachment.ext]`|`[attachment.ext](attachment.ext)`|\n|`[http://www.example.com]`|`<http://www.example.com>`|\n|`[Example\\|http://example.com]`|`[Example](http://example.com)`|\n|`[mailto:box@example.com]`|`<box@example.com>`|\n|`[file:///c:/temp/foo.txt]`|Not converted|\n|`{anchor:anchorname}`|Not converted|\n|`[~username]`|`@username`|\n\n## Lists\n\n<table>\n<tr>\n<th>Jira</th>\n<th>Markdown</th>\n</tr>\n<tr>\n<td>\n\n```\n* some\n* bullet\n** indented\n** bullets\n* points\n```\n</td>\n<td>\n\n```\n- some\n- bullet\n  - indented\n  - bullets\n- points\n```\n</td>\n</tr>\n<tr>\n<td>\n\n```\n# a\n# numbered\n# list\n```\n</td>\n<td>\n\n```\n1. a\n1. numbered\n1. list\n```\n</td>\n</tr>\n<tr>\n<td>\n\n```\n# a\n# numbered\n#* with\n#* nested\n#* bullet\n# list\n```\n</td>\n<td>\n\n```\n1. a\n1. numbered\n   - with\n   - nested\n   - bullet\n1. list\n```\n</td>\n</tr>\n<tr>\n<td>\n\n```\n* a\n* bulleted\n*# with\n*# nested\n*# numbered\n* list\n```\n</td>\n<td>\n\n```\n- a\n- bulleted\n  1. with\n  1. nested\n  1. numbered\n- list\n```\n</td>\n</tr>\n</table>\n\n## Images\n\n| Jira | Markdown |\n|------|----------|\n|`!image.jpg!`|`![image.jpg](image.jpg)`|\n|`!image.jpg\\|thumbnail!`|`![image.jpg](image.jpg)`|\n|`!image.jpg\\|width=300,height=200!`|`![image.jpg](image.jpg){width=300}{height=200}`|\n\nOnly `width` and `height` attributes are supported.\n\n## Tables\n\n<table>\n<tr>\n<th>Jira</th>\n<th>Markdown</th>\n</tr>\n<tr>\n<td>\n\n```\n||heading 1||heading 2||heading 3||\n|col A1|col A2|col A3|\n|col B1|col B2|col B3|\n\n```\n</td>\n<td>\n\n```\n|heading 1|heading 2|heading 3|\n|-|-|-|\n|col A1|col A2|col A3|\n|col B1|col B2|col B3|\n```\n</td>\n</tr>\n</table>\n\n## Advanced Formatting\n\n<table>\n<tr>\n<th>Jira</th>\n<th>Markdown</th>\n</tr>\n<tr>\n<td>\n\n```\n{noformat}\npreformatted piece of text\n so *no* further _formatting_ is done here\n{noformat}\n```\n</td>\n<td>\n\n````\n```\npreformatted piece of text\n so *no* further _formatting_ is done here\n```\n````\n</td>\n</tr>\n<tr>\n<td>\n\n```\n{panel}\nSome text\n{panel}\n```\n</td>\n<td>Not supported</td>\n</tr>\n<tr>\n<td>\n\n```\n{code:xml}\n    <test>\n        <another tag="attribute"/>\n    </test>\n{code}\n```\n</td>\n<td>\n\n````\n```xml\n    <test>\n        <another tag="attribute"/>\n    </test>\n```\n````\n</td>\n</tr>\n</table>\n',
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
