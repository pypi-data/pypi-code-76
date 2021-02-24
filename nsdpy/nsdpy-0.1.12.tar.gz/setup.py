# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['nsdpy']
install_requires = \
['certifi>=2020.12.5,<2021.0.0',
 'chardet>=4.0.0,<5.0.0',
 'idna>=2.10,<3.0',
 'requests>=2.25.1,<3.0.0',
 'urllib3>=1.26.2,<2.0.0']

entry_points = \
{'console_scripts': ['nsdpy = nsdpy:main']}

setup_kwargs = {
    'name': 'nsdpy',
    'version': '0.1.12',
    'description': 'Automatize the donwload of DNA sequences from NCBI, sort them according to their taxonomy and filter them with a gene name (provided as a regular expression)',
    'long_description': '# NucleoPy\n\n- [Introduction](#introduction)\n- [workfolw](#workflow)\n- [Installation](#installation)\n- [Usage](#usage)\n  - [Google Colab](#on-google-colab)\n  - [Command line](#command-line)\n- [Authors and acknowledgment](#authors-and-acknowledgment)\n- [Support](#support)\n- [Licence](#license)\n- [More Documentation](#more-documentation)\n\n\n\n## Introduction\n\nNucleoPy aims to ease the download and sort of big bacth of DNA sequences from the NCBI database. \nIt can also be usefull to filter the sequences based on their annotations.\nUsing NucleoPy the user can:\n\n- **Search** NCBI nucleotide database\n- **Download** the fasta files or the cds_fasta files corresponding to the result of the search\n- **Sort** the sequences based on their taxonomy\n- **Filter** the sequences based on the name of the gene by giving one or more regular expression as filter(s)\n\n## Workflow\n\n<img src="https://github.com/RaphaelHebert/Nucleopy/blob/options/workflow.png" alt="workflow" width="600"/>\n\n## Installation \n\nThe package will be available from PyPI soon. \n\nexepected:\n\n```bash\npip3 install nucleopy\n```\n\n## Usage\n### On google colab:\n[Nucleopy colab notebook](https://colab.research.google.com/drive/1UmxzRc_k5sNeQ2RPGe29nWR_1_0FRPkq?usp=sharing)\n\n### Command line\n\n```bash\n      python3 main.py -r USER\'S REQUEST [OPTIONS] \n```\n\n## Authors and acknowledgment\n\n## Support\n\n## License\nto choose, probably: https://choosealicense.com/licenses/gpl-3.0/\n\n\n## More Documentation\n\nFor examples of usage and more detailed documentation check: \n[Users manual on google doc](https://docs.google.com/document/d/1CJQg2Cv3P0lgWZRYd9xJQfj8qwIY4a-wtXa4VERdH2c/edit?usp=sharing =100)\n\n\n',
    'author': 'RaphaelHebert',
    'author_email': 'raphaelhebert18@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/RaphaelHebert/nsdpy',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.5,<4.0.0',
}


setup(**setup_kwargs)
