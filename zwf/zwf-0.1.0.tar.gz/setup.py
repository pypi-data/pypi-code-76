# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['zwf']
install_requires = \
['docopt>=0.6.2,<0.7.0', 'hurry.filesize>=0.9,<0.10']

entry_points = \
{'console_scripts': ['zwf = zwf:main']}

setup_kwargs = {
    'name': 'zwf',
    'version': '0.1.0',
    'description': 'Tools for Zwift WAD files',
    'long_description': '# zwf — Zwift WAD file tool\n\nA tool to list/extract files from Zwift WAD files — the asset archives (like a tar/zip file) that Zwift uses.\n\n## Limitations\n\n**Compressed .wad files are not supported**. The .wad files which ship with Zwift under `assets/**/*.wad` are compressed. This tool can work with the decompressed versions, but does not implement decompression itself. \n\nYou might find decompressed versions in a memory dump of a Zwift process, but that may be against the Zwift TOS.\n',
    'author': 'Hal Blackburn',
    'author_email': 'hal.blackburn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/h4l/zwf',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
