# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autowoe',
 'autowoe.lib',
 'autowoe.lib.cat_encoding',
 'autowoe.lib.optimizer',
 'autowoe.lib.pipelines',
 'autowoe.lib.report',
 'autowoe.lib.report.utilities_images',
 'autowoe.lib.selectors',
 'autowoe.lib.types_handler',
 'autowoe.lib.utilities',
 'autowoe.lib.woe']

package_data = \
{'': ['*']}

install_requires = \
['jinja2',
 'joblib',
 'lightgbm',
 'matplotlib',
 'numpy',
 'pandas',
 'pytest',
 'pytz',
 'scikit-learn',
 'scipy',
 'seaborn',
 'sphinx',
 'sphinx-rtd-theme']

setup_kwargs = {
    'name': 'autowoe',
    'version': '1.2.4',
    'description': 'Library for automatic interpretable model building (Whitebox AutoML)',
    'long_description': '## Sberbank version of AutoWoE\n\n![GitHub all releases](https://img.shields.io/github/downloads/sberbank-ai-lab/AutoMLWhitebox/total?color=green&logo=github&style=plastic)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/autowoe?color=green&label=PyPI%20downloads&logo=pypi&logoColor=orange&style=plastic)\n\n\nThis is the repository for **AutoWoE** library, developed by Sber AI Lab AutoML group. This library can be used for automatic creation of interpretable ML model based on feature binning, WoE features transformation, feature selection and Logistic Regression.\n\n**Authors:** Vakhrushev Anton, Grigorii Penkin\n\n**Library setup** can be done by one of three scenarios below:\n- `pip install autowoe` for installation from PyPI\n- `bash build_package.sh` for library installation into automatically created virtual environment and WHL files building\n- pre-generated WHL file from specific release \n\n**Usage tutorials** are in Jupyter notebooks in the repository root. For **parameters description** take a look at `parameters_info.md`.\n\n**Bugs / Questions / Suggestions:**:\n- Vakhrushev Anton (AGVakhrushev@sberbank.ru)\n',
    'author': 'Vakhrushev Anton',
    'author_email': 'AGVakhrushev@sberbank.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sberbank-ai-lab/AutoMLWhitebox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
