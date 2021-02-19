# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['printfactory', 'printfactory.print_tools']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7.3,<2.0.0']

setup_kwargs = {
    'name': 'printfactory',
    'version': '0.1.2a0',
    'description': 'Print PDF files to a local installed printer using a print tool',
    'long_description': '# printfactory\n\n`printfactory` is a package for printing PDF files to a physical printer \nusing a print tool like [Adobe Reader][AdobeReader] or [Foxit Reader][FoxitReader].\n\n[![License?][shield-license]](LICENSE)\n\n**Example usage**\n\n    import pathlib\n    import printfactory\n    \n    printer = printfactory.Printer()\n    print_tool = printfactory.AdobeReader(printer)\n    \n    file = pathlib.Path(\'my.pdf\')\n    print_tool.print_file(file)\n\n## Table of Contents\n\n- [Why?](#why)\n- [Requirements](#requirements)\n- [Installing `printfactory`](#installing-printfactory)\n- [Known issues](#known-issues)\n- [Contributing](#contributing)\n- [Changelog](#changelog)\n\n## Why?\n\nThe motivation for this project was to have a simple Python interface\nfor printing PDF files to a physical printer using a local installed software _("print-tool")_.\n\nOnly publicly and freely available software should be used on the client or server that is using this package.\n\n## Requirements\n\n- [Python >= 3.8][python]\n- [pip][pip]\n\n## Installing `printfactory`\n\nTo install the latest version of `printfactory` use pip as simple as follows.\n\n    pip install printfactory\n\n## Known issues\n\n- The _AdobeAcrobat_ print tool implementation is limited to only send files to the defaults system printer\n\n## Contributing\n\nIf you\'d like to contribute to this project [Poetry][poetry] is recommended.\n\n## Changelog\n\nAll notable changes to this project will be documented in the [CHANGELOG.md](CHANGELOG.md).\n\n\n\n[shield-license]: https://img.shields.io/badge/license-MIT-blue.svg\n\n[AdobeReader]: https://get.adobe.com/reader/\n[FoxitReader]: https://www.foxitsoftware.com/pdf-reader/\n\n[python]: https://www.python.org/\n[pip]: https://pypi.org/project/pip/\n[poetry]: https://python-poetry.org/\n',
    'author': 'dl6nm',
    'author_email': 'mail@dl6nm.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dl6nm/printfactory',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
