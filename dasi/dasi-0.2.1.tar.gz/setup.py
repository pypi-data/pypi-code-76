# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dasi',
 'dasi.command_line',
 'dasi.cost',
 'dasi.design',
 'dasi.models',
 'dasi.schemas',
 'dasi.utils',
 'dasi.utils.biopython',
 'dasi.utils.networkx',
 'dasi.utils.sequence']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.78,<2.0',
 'frozendict>=1.2,<2.0',
 'jdna>=0.2,<0.3',
 'jsonschema>=3.1,<4.0',
 'loggable-jdv>=0.1.5,<0.2.0',
 'matplotlib>=3.1,<4.0',
 'more-itertools>=8.0,<9.0',
 'msgpack-numpy>=0.4.4,<0.5.0',
 'msgpack>=0.6.1,<0.7.0',
 'networkx>=2.3,<3.0',
 'numpy>=1.17,<2.0',
 'primer3plus>=1.0.8,<2.0.0',
 'pyblastbio>=0.9,<0.10',
 'sympy>=1.4,<2.0',
 'tqdm>=4.32,<5.0']

extras_require = \
{':python_version >= "3.7" and python_version < "4.0"': ['pandas>=1.1.0,<2.0.0'],
 'documentation': ['nbsphinx>=0.4.2,<0.5.0',
                   'sphinx_autodoc_typehints>=1.8,<2.0',
                   'sphinx-jsonschema>=1.11,<2.0',
                   'sphinx>=2.2,<3.0',
                   'sphinx-bootstrap-theme>=0.7.1,<0.8.0'],
 'styling': ['pre-commit>=1.17,<2.0',
             'flake8>=3.7,<4.0',
             'black>=20.8b1,<21.0']}

entry_points = \
{'console_scripts': ['dasi = dasi:command_line.main']}

setup_kwargs = {
    'name': 'dasi',
    'version': '0.2.1',
    'description': 'Automated DNA assembly planner for Python',
    'long_description': "# DASi DNA Design\n\n[![PyPI version](https://badge.fury.io/py/dasi.svg)](https://badge.fury.io/py/dasi)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n![Build package](https://github.com/jvrana/DASi-DNA-Design/workflows/Build%20package/badge.svg)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/jvrana/DASi-DNA-Design.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/jvrana/DASi-DNA-Design/context:python)\n[![Total alerts](https://img.shields.io/lgtm/alerts/g/jvrana/DASi-DNA-Design.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/jvrana/DASi-DNA-Design/alerts/)\n\n**DASi** is an automatic DNA cloning plan designer aimed for operating on small budgets\nby focusing on material re-use.\n\nThe software converts a nucleotide sequence, or a library of sequences, to an executable\n molecular assembly plan while optimizing material cost, assembly efficiency, and assembly time.\n\nThe key design paradigm for DASi is that *no molecular biology expertise* is required to use DASi. Complete novices should be able to use the software to design and construct new genetic sequences. This also enables automated software programs to automatically design and construct new genetic sequences.\n\nThe software goals are reminiscent of j5 or Teselegen but focused on:\n1. A dead-simple API usable by lab novices, experts or automated software programs.\n1. Utilizing information about current laboratory inventory in its optimization\nalgorithm to minimize costs and turn-around time\n\n### Status\n\nDASi is currently under development funded by the DARPA Synergistic Discovery and Design program. DASi is currently being used to connect automatically generate DNA designs to automated biological fabrication facilities (e.g. University of Washington Biofab).\n\n### Usage\n\nDASi completely automates the cloning design work, finding approximately optimal solutions for cloning steps, preferentially using existing plasmids, linear DNA fragments, and primers to design semi-optimal cloning steps and designs.\n\nThe following command designs the cloning steps for a library of designs. The user only needs to specify the sequences they wish to construct and currently available primers and DNA templates as *.genbank* or *.fasta* files. DASi handles all design aspects. *No molecular biology expertise is required to use DASi.*\n\n```bash\ndasi library_design --designs mydesigns/*.gb --fragments fragments/*.gb --primers primers.fasta --templates plasmids/*.gb --cost_model cost.b --out results\n```\n\n#### Customization\n\nDASi optimization parameters are completely customizable. The following are examples of parameters and aspects of DASi that are customizable:\n\n* primer synthesis costs\n* primer design parameters\n* synthetic fragment costs\n* vendor-specific synthetic fragment complexity\n* sequence dependent plasmid assembly efficiencies\n* optimizing over efficiency vs material costs\n* etc.\n\n### Planned Features\n\n* Golden-gate support\n* heirarchical assembly\n* library support (with bayesian search to optimize shared parts)\n* front-end\n* connection to fabrication facility\n\n### DASi optimization problem\n\nBriefly, DASi approximates a solution the following optimization problem: \n\n```Given a set of 'goal' double-stranded sequences, a set of available single-stranded and double-strand sequences, and a set of actions that can create new sequences, find the optimal set of operations that produces the 'goal' sequences.```\n\nFormalization of this optimization problem is coming soon.\n",
    'author': 'Justin Vrana',
    'author_email': 'justin.vrana@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jvrana/dasi-dna-design',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
