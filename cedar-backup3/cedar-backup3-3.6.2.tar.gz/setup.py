# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['CedarBackup3',
 'CedarBackup3.actions',
 'CedarBackup3.extend',
 'CedarBackup3.tools',
 'CedarBackup3.writers']

package_data = \
{'': ['*']}

install_requires = \
['chardet>=3.0.4,<4.0.0']

entry_points = \
{'console_scripts': ['cback3 = CedarBackup3.scripts:cback3',
                     'cback3-amazons3-sync = CedarBackup3.scripts:amazons3',
                     'cback3-span = CedarBackup3.scripts:span']}

setup_kwargs = {
    'name': 'cedar-backup3',
    'version': '3.6.2',
    'description': 'Implements local and remote backups to CD/DVD and Amazon S3',
    'long_description': '[![pypi](https://img.shields.io/pypi/v/cedar-backup3.svg)](https://pypi.org/project/cedar-backup3/)\n[![license](https://img.shields.io/pypi/l/cedar-backup3.svg)](https://github.com/pronovic/cedar-backup3/blob/master/LICENSE)\n[![wheel](https://img.shields.io/pypi/wheel/cedar-backup3.svg)](https://pypi.org/project/cedar-backup3/)\n[![python](https://img.shields.io/pypi/pyversions/cedar-backup3.svg)](https://pypi.org/project/cedar-backup3/)\n[![Test Suite](https://github.com/pronovic/cedar-backup3/workflows/Test%20Suite/badge.svg)](https://github.com/pronovic/cedar-backup3/actions?query=workflow%3A%22Test+Suite%22)\n[![docs](https://readthedocs.org/projects/cedar-backup3/badge/?version=stable&style=flat)](https://cedar-backup3.readthedocs.io/en/stable/)\n[![coverage](https://coveralls.io/repos/github/pronovic/cedar-backup3/badge.svg?branch=master)](https://coveralls.io/github/pronovic/cedar-backup3?branch=master)\n\n[Cedar Backup](https://github.com/pronovic/cedar-backup3) is a software package\ndesigned to manage system backups for a pool of local and remote machines.\nCedar Backup understands how to back up filesystem data as well as MySQL and\nPostgreSQL databases and Subversion repositories.  It can also be easily\nextended to support other kinds of data sources.\n\nCedar Backup is focused around weekly backups to a single CD or DVD disc,\nwith the expectation that the disc will be changed or overwritten at the\nbeginning of each week.  If your hardware is new enough, Cedar Backup can\nwrite multisession discs, allowing you to add incremental data to a disc on\na daily basis.  Alternately, Cedar Backup can write your backups to the Amazon\nS3 cloud rather than relying on physical media.  See \nthe [Cedar Backup v3 Software Manual](https://cedar-backup3.readthedocs.io/en/stable/manual/index.html) for details.\n\nBesides offering command-line utilities to manage the backup process, Cedar\nBackup provides a well-organized library of backup-related functionality.\nFor more information, see \nthe [API Reference](https://cedar-backup3.readthedocs.io/en/stable/autoapi/index.html).\n\nThere are many different backup software systems in the open source world.\nCedar Backup aims to fill a niche: it aims to be a good fit for people who need\nto back up a limited amount of important data on a regular basis. Cedar Backup\nisn’t for you if you want to back up your huge MP3 collection every night, or\nif you want to back up a few hundred machines.  However, if you administer a\nsmall set of machines and you want to run daily incremental backups for things\nlike system configuration, current email, small web sites, source code\nrepositories, or small databases, then Cedar Backup is probably worth your\ntime.\n',
    'author': 'Kenneth J. Pronovici',
    'author_email': 'pronovic@ieee.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/cedar-backup3/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
