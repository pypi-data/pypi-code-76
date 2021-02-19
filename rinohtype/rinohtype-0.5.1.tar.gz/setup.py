# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rinoh',
 'rinoh.backend',
 'rinoh.backend.pdf',
 'rinoh.backend.pdf.xobject',
 'rinoh.backend.pdf.xobject.icc',
 'rinoh.font',
 'rinoh.font.opentype',
 'rinoh.fonts',
 'rinoh.frontend',
 'rinoh.frontend.commonmark',
 'rinoh.frontend.docbook',
 'rinoh.frontend.epub',
 'rinoh.frontend.rst',
 'rinoh.frontend.sphinx',
 'rinoh.frontend.xml',
 'rinoh.language',
 'rinoh.stylesheets',
 'rinoh.templates']

package_data = \
{'': ['*'],
 'rinoh': ['data/fonts/*',
           'data/fonts/adobe14/*',
           'data/hyphen/*',
           'data/stylesheets/*',
           'data/xml/*',
           'data/xml/docutils/*',
           'data/xml/w3c-entities/*']}

install_requires = \
['appdirs>=1.4.3,<2.0.0',
 'docutils>=0.15',
 'recommonmark>=0.6.0',
 'rinoh-typeface-dejavuserif>=0.1.3,<0.2.0',
 'rinoh-typeface-texgyrecursor>=0.1.1,<0.2.0',
 'rinoh-typeface-texgyreheros>=0.1.1,<0.2.0',
 'rinoh-typeface-texgyrepagella>=0.1.1,<0.2.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=0.21']}

entry_points = \
{'console_scripts': ['rinoh = rinoh.__main__:main'],
 'rinoh.frontends': ['CommonMark = rinoh.frontend.commonmark:CommonMarkReader',
                     'reStructuredText = '
                     'rinoh.frontend.rst:ReStructuredTextReader'],
 'rinoh.stylesheets': ['sphinx = rinoh.stylesheets:sphinx',
                       'sphinx_article = rinoh.stylesheets:sphinx_article',
                       'sphinx_base14 = rinoh.stylesheets:sphinx_base14'],
 'rinoh.templates': ['article = rinoh.templates:Article',
                     'book = rinoh.templates:Book'],
 'rinoh.typefaces': ['courier = rinoh.fonts.adobe14:courier',
                     'helvetica = rinoh.fonts.adobe14:helvetica',
                     'itc zapfdingbats = rinoh.fonts.adobe14:zapfdingbats',
                     'symbol = rinoh.fonts.adobe14:symbol',
                     'times = rinoh.fonts.adobe14:times'],
 'sphinx.builders': ['rinoh = rinoh.frontend.sphinx']}

setup_kwargs = {
    'name': 'rinohtype',
    'version': '0.5.1',
    'description': 'The Python document processor',
    'long_description': "rinohtype\n=========\n\n.. image:: http://img.shields.io/pypi/v/rinohtype.svg\n   :target: https://pypi.python.org/pypi/rinohtype\n   :alt: PyPI\n\n.. image:: https://img.shields.io/pypi/pyversions/rinohtype.svg\n   :target: https://pypi.python.org/pypi/rinohtype\n   :alt: Python version\n\n.. image:: https://badges.gitter.im/brechtm/rinohtype.svg\n   :target: https://gitter.im/brechtm/rinohtype\n   :alt: Gitter chat\n\n.. image:: https://github.com/brechtm/rinohtype/workflows/Test%20&%20Publish/badge.svg\n   :target: https://github.com/brechtm/rinohtype/actions?query=workflow%3A%22Test+%26+Publish%22\n   :alt: Tests\n\n.. image:: https://codecov.io/gh/brechtm/rinohtype/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/brechtm/rinohtype\n   :alt: Test coverage\n\n\nrinohtype is a batch-mode document processor. It renders structured documents\nto PDF based on a document template and a style sheet. An important design goal\nof rinohtype is make document layout and style customization user-friendly. See\nthe documentation_ to learn how to customize the style of your document.\n\n\nCall for Contributions\n----------------------\n\nSince rinohtype is a fairly sizable project and currently being maintained by a\nsingle person, your contribution can make a big difference. Specifically, the\nfollowing things can help move rinohtype forward:\n\n* development of professional-looking stylesheets and document templates\n* volunteering to be a maintainer: fix issues that pop up when new versions of\n  dependencies are released (Python, Sphinx, ...)\n* help with maintaining and improving the documentation\n* development of new features, e.g. widow/orphan handling, Knuth-Plass line\n  breaking, mathematics typesetting, performance improvements, ...\n* companies might be interested in funding the development of particular\n  features that would benefit them\n\nSo if you are interested in helping with any of these items, please don't\nhesitate to get in touch via brecht@opqode.com, `GitHub issues`_ or Gitter_!\n\n.. _GitHub issues: https://github.com/brechtm/rinohtype/issues\n.. _Gitter: https://gitter.im/brechtm/rinohtype\n\n\nFeatures\n--------\n\nrinohtype is still in beta, so you might run into some issues when using it.\nI'd highly appreciate it if you could `create a ticket`_ for any bugs you may\nencounter. That said, rinohtype is already quite capable. For example, it\nshould be able to replace Sphinx_'s LaTeX builder in most cases. Here is an\noverview of the main features:\n\n* a powerful page layout system supporting columns, running headers/footers,\n  floatable elements and footnotes\n* support for figures and (large) tables\n* automatic generation of table of contents and index\n* automatic numbering and cross-referencing of section headings, figures and\n  tables\n* configure one of the included document templates or create your own\n* an intuitive style sheet system inspired by CSS\n* modular design allowing for multiple frontends (such as reStructuredText,\n  Markdown, DocBook, ...)\n* handles OpenType, TrueType and Type1 fonts with support for advanced\n  typographic features such as kerning, ligatures, small capitals and old style\n  figures\n* embeds PDF, PNG and JPEG images, preserving transparency and color profiles\n* easy to install and deploy; pure-Python with few dependencies\n* built on Unicode; ready for non-latin languages\n\nrinohtype's primary input format is reStructuredText_. The ``rinoh`` command\nline tool renders reStructuredText documents and the included Sphinx_ builder\nmakes it possible to output large documents with your own style applied. Have\na look at the `rinohtype documentation`_ for an example of the output.\n\n.. _documentation: http://www.mos6581.org/rinohtype/master/\n.. _create a ticket: https://github.com/brechtm/rinohtype/issues/new/choose\n.. _reStructuredText: http://docutils.sourceforge.net/rst.html\n.. _Sphinx: http://sphinx-doc.org\n.. _rinohtype documentation: http://www.mos6581.org/rinohtype/master/_downloads/cc8bb3ec0357396958ad856a90d03812/rinohtype.pdf\n\n\nRequirements\n------------\n\nrinohtype supports all stable Python 3 versions that have not reached\nend-of-life_ status. For parsing reStructuredText and CommonMark documents,\nrinohtype depends on docutils_ and recommonmark_ respectively. pip_ takes care\nof installing these requirements when you install rinohtype.\n\nSyntax highlighting of code blocks is eneabled if Pygments_ is installed, which\nwill be installed automatically with Sphinx_. If you want to include images\nother than PDF, PNG or JPEG, you also need to install Pillow_.\n\n.. _end-of-life: https://devguide.python.org/#status-of-python-branches\n.. _docutils: http://docutils.sourceforge.net/index.html\n.. _recommonmark: https://recommonmark.readthedocs.io\n.. _pip: https://pip.pypa.io\n.. _Pygments: https://pygments.org\n.. _Pillow: http://python-pillow.github.io\n\n\nGetting Started\n---------------\n\nInstallation is trivial::\n\n    pip install rinohtype\n\n\nreStructuredText Renderer\n~~~~~~~~~~~~~~~~~~~~~~~~~\n\nThe easiest way to get started with rinohtype is to render a reStructuredText\ndocument (such as ``CHANGES.rst`` from this repository) using the ``rinoh``\ncommand line tool::\n\n   rinoh CHANGES.rst\n\nWhen ``rinoh`` finishes, you will find ``CHANGES.pdf`` alongside the input\nfile.\n\nBy default ``rinoh`` renders the input document using the article template. Run\n``rinoh --help`` to see how you can tell ``rinoh`` which document template and\nstyle sheet to use.\n\n\nSphinx Builder\n~~~~~~~~~~~~~~\n\nrinohtype can be used as a drop-in replacement for the LaTeX builder (the\n``latex_documents`` configuration variable has to be set). Simply select the\n`rinoh` builder when building the Sphinx project::\n\n    sphinx-build -b rinoh . _build/rinoh\n\n\nContributing\n------------\n\nSee ``CONTRIBUTING.rst`` and ``DEVELOPING.rst``\n\n\nLicense\n-------\n\nAll of rinohtype's source code is licensed under the `Affero GPL 3.0`_, unless\nindicated otherwise in the source file (such as ``hyphenator.py`` and\n``purepng.py``).\n\nThe Affero GPL requires for software that builds on rinohtype to also be\nreleased as open source under this license. For building closed-source\napplications, you can obtain a `commercial license`_. The author of rinohtype\nis also available for consultancy projects involving rinohtype.\n\n.. _Affero GPL 3.0: https://www.gnu.org/licenses/agpl-3.0.html\n.. _commercial license: brecht.machiels@opqode.com\n",
    'author': 'Brecht Machiels',
    'author_email': 'brecht@mos6581.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/brechtm/rinohtype',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
