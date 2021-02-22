# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unmarkd']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0']

setup_kwargs = {
    'name': 'unmarkd',
    'version': '0.1.1',
    'description': 'A markdown reverser.',
    'long_description': '# 🔄 Unmarkd\n[![codecov](https://codecov.io/gh/ThatXliner/unmarkd/branch/master/graph/badge.svg?token=PWVIERHTG3)](https://codecov.io/gh/ThatXliner/unmarkd)\n\n> A markdown reverser.\n\n---\nUnmarkd is a [BeautifulSoup](https://github.com/ThatXliner/unmarkd/issues/4)-powered [Markdown](https://en.wikipedia.org/wiki/Markdown) reverser written in Python and for Python. There are [similar projects](https://github.com/xijo/reverse_markdown) (written in Ruby) but I have not found any written in Python (or for Python).\n\n## Why\n\nThis is created as a [StackSearch](http://github.com/ThatXliner/stacksearch) (one of my other projects) dependancy.\n\nIn order to create a better API, I needed a way to reverse HTML. So I created this.\n\n## Installation\n\nYou know the drill\n\n```bash\npip install unmarkd\n```\n\n## Known issues\n\n - Nested lists are not properly indented ([#4](https://github.com/ThatXliner/unmarkd/issues/4))\n\n## Documentation\n\nHere\'s an example of basic usage\n\n```python\nimport unmarkd\nprint(unmarkd.unmark("<b>I <i>love</i> markdown!</b>"))\n# Output: **I *love* markdown!**\n```\n\nor something more complex (shamelessly taken from [here](https://markdowntohtml.com)):\n\n```python\nimport unmarkd\nhtml_doc = R"""<h1 id="sample-markdown">Sample Markdown</h1>\n<p>This is some basic, sample markdown.</p>\n<h2 id="second-heading">Second Heading</h2>\n<ul>\n<li>Unordered lists, and:<ol>\n<li>One</li>\n<li>Two</li>\n<li>Three</li>\n</ol>\n</li>\n<li>More</li>\n</ul>\n<blockquote>\n<p>Blockquote</p>\n</blockquote>\n<p>And <strong>bold</strong>, <em>italics</em>, and even <em>italics and later <strong>bold</strong></em>. Even <del>strikethrough</del>. <a href="https://markdowntohtml.com">A link</a> to somewhere.</p>\n<p>And code highlighting:</p>\n<pre><code class="lang-js"><span class="hljs-keyword">var</span> foo = <span class="hljs-string">\'bar\'</span>;\n\n<span class="hljs-function"><span class="hljs-keyword">function</span> <span class="hljs-title">baz</span><span class="hljs-params">(s)</span> </span>{\n   <span class="hljs-keyword">return</span> foo + <span class="hljs-string">\':\'</span> + s;\n}\n</code></pre>\n<p>Or inline code like <code>var foo = &#39;bar&#39;;</code>.</p>\n<p>Or an image of bears</p>\n<p><img src="http://placebear.com/200/200" alt="bears"></p>\n<p>The end ...</p>\n"""\nprint(unmarkd.unmark(html_doc))\n```\nand the output:\n\n    # Sample Markdown\n\n    This is some basic, sample markdown.\n\n    ## Second Heading\n\n\n     * Unordered lists, and:\n     0. One\n     1. Two\n     2. Three\n     * More\n    > Blockquote\n\n    And **bold**, *italics*, and even *italics and later **bold***. Even ~~strikethrough~~. [A link](https://markdowntohtml.com) to somewhere.\n    And code highlighting:\n\n    ```js\n    var foo = \'bar\';\n\n    function baz(s) {\n       return foo + \':\' + s;\n    }\n\n    ```\n\n    Or inline code like `var foo = \'bar\';`.\n    Or an image of bears\n    ![bears](http://placebear.com/200/200)\n    The end ...\n\n### Extending\n\n#### Brief Overview\n\nMost functionality should be covered by the `BasicUnmarker` class defined in `unmarkd.unmarkers`.\n\nIf you need to reverse markdown from StackExchange (as in the case for my other project), you may use the `StackOverflowUnmarker` (or it\'s alias, `StackExchangeUnmarker`), which is also defined in `unmarkd.unmarkers`.\n\n#### Customizing\n\nIf the above two classes do not suit your needs, you can subclass the `unmarkd.unmarkers.BaseUnmarker` abstract class.\n\nCurrently, you *must* define the following methods:\n\n - `detect_language` (parameters: **1**)\n    - When a fenced code block is approached, this function is called with a parameter of type `bs4.BeautifulSoup` passed to it; this is the element the code block was detected from (i.e. `pre`).\n    - This function is responsible for detecting the programming language (or returning `\'\'` if none was detected) of the code block.\n\n\nCurrently, there are no methods you can *optionally* override.\n',
    'author': 'Bryan Hu',
    'author_email': 'bryan.hu.2020@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ThatXliner/unmarkd/tree/master',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
