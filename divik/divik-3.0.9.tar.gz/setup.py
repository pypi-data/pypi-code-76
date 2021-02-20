# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['divik',
 'divik._cli',
 'divik.cluster',
 'divik.cluster._divik',
 'divik.cluster._kmeans',
 'divik.core',
 'divik.core.io',
 'divik.feature_extraction',
 'divik.feature_selection',
 'divik.feature_selection._exims',
 'divik.sampler',
 'divik.score']

package_data = \
{'': ['*']}

install_requires = \
['dask-distance>=0.2.0,<0.3.0',
 'dask[dataframe]>=2.14.0',
 'h5py>=2.8.0',
 'joblib>=1.0.0,<2.0.0',
 'kneed>=0.5.1',
 'matplotlib>=3.3.3,<4.0.0',
 'numpy>=0.12.1',
 'pandas>=0.20.3',
 'scikit-image>=0.14.1',
 'scikit-learn>=0.19.0',
 'scipy>=0.19.1',
 'tqdm>=4.11.2']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0'],
 'all': ['polyaxon>=1.5.0,<2.0.0', 'gin-config>=0.4.0,<0.5.0'],
 'gin': ['gin-config>=0.4.0,<0.5.0'],
 'polyaxon': ['polyaxon>=1.5.0,<2.0.0']}

entry_points = \
{'console_scripts': ['fit-clusters = divik._cli.fit_clusters:main']}

setup_kwargs = {
    'name': 'divik',
    'version': '3.0.9',
    'description': 'Divisive iK-means algorithm implementation',
    'long_description': '[![CodeFactor](https://www.codefactor.io/repository/github/gmrukwa/divik/badge)](https://www.codefactor.io/repository/github/gmrukwa/divik)\n[![BCH compliance](https://bettercodehub.com/edge/badge/gmrukwa/divik?branch=master)](https://bettercodehub.com/)\n[![Maintainability](https://api.codeclimate.com/v1/badges/4cf5d42d0a0076c38445/maintainability)](https://codeclimate.com/github/gmrukwa/divik/maintainability)\n![](https://github.com/gmrukwa/divik/workflows/Build%20and%20push%20deployment%20images/badge.svg)\n![](https://github.com/gmrukwa/divik/workflows/Run%20unit%20tests/badge.svg)\n[![Documentation Status](https://readthedocs.org/projects/divik/badge/?version=latest)](https://divik.readthedocs.io/en/latest/?badge=latest)\n\n# divik\n\nPython implementation of Divisive iK-means (DiviK) algorithm.\n\n## Tools within this package\n\n- Clustering at your command line with fit-clusters\n- Set of algorithm implementations for unsupervised analyses\n  - Clustering\n    - DiviK - hands-free clustering method with built-in feature selection\n    - K-Means with Dunn method for selecting the number of clusters\n    - K-Means with GAP index for selecting the number of clusters\n    - Modular K-Means implementation with custom distance metrics and initializations\n  - Feature extraction\n    - PCA with knee-based components selection\n    - Locally Adjusted RBF Spectral Embedding\n  - Feature selection\n    - EXIMS\n    - Gaussian Mixture Model based data-driven feature selection\n      - High Abundance And Variance Selector - allows you to select highly variant features above noise level, based on GMM-decomposition\n    - Outlier based Selector\n      - Outlier Abundance And Variance Selector - allows you to select highly variant features above noise level, based on outlier detection\n    - Percentage based Selector - allows you to select highly variant features above noise level with your predefined thresholds for each\n  - Sampling\n    - StratifiedSampler - generates samples of fixed number of rows from given dataset\n    - UniformPCASampler - generates samples of random observations within boundaries of an original dataset, and preserving the rotation of the data\n    - UniformSampler - generates samples of random observations within boundaries of an original dataset\n\n## Installation\n\n### Docker\n\nThe recommended way to use this software is through\n[Docker](https://www.docker.com/). This is the most convenient way, if you want\nto use `divik` application.\n\nTo install latest stable version use:\n\n```bash\ndocker pull gmrukwa/divik\n```\n\n### Python package\n\nPrerequisites for installation of base package:\n\n- Python 3.6 / 3.7 / 3.8\n- compiler capable of compiling the native C code and OpenMP support\n\n#### Installation of OpenMP for Ubuntu / Debian\n\nYou should have it already installed with GCC compiler, but if somehow\nnot, try the following:\n\n```bash\nsudo apt-get install libgomp1\n```\n\n#### Installation of OpenMP for Mac\n\nOpenMP is available as part of LLVM. You may need to install it with conda:\n\n```bash\nconda install -c conda-forge "compilers>=1.0.4,!=1.1.0" llvm-openmp\n```\n\n#### DiviK Installation\n\nHaving prerequisites installed, one can install latest base version of the\npackage:\n\n```bash\npip install divik\n```\n\nIf you want to have compatibility with\n[`gin-config`](https://github.com/google/gin-config), you can install\nnecessary extras with:\n\n```bash\npip install divik[gin]\n```\n\n**Note:** Remember about `\\` before `[` and `]` in `zsh` shell.\n\nYou can install all extras with:\n\n```bash\npip install divik[all]\n```\n\n## High-Volume Data Considerations\n\nIf you are using DiviK to run the analysis that could fail to fit RAM of your\ncomputer, consider disabling the default parallelism and switch to\n[dask](https://dask.org/). It\'s easy to achieve through configuration:\n\n- set all parameters named `n_jobs` to `1`;\n- set all parameters named `allow_dask` to `True`.\n\n**Note:** Never set `n_jobs>1` and `allow_dask=True` at the same time, the\ncomputations will freeze due to how `multiprocessing` and `dask` handle\nparallelism.\n\n## Known Issues\n\n### Segmentation Fault\n\nIt can happen if the he `gamred_native` package (part of `divik` package) was\ncompiled with different numpy ABI than scikit-learn. This could happen if you\nused different set of compilers than the developers of the scikit-learn\npackage.\n\nIn such a case, a handler is defined to display the stack trace. If the trace\ncomes from `_matlab_legacy.py`, the most probably this is the issue.\n\nTo resolve the issue, consider following the installation instructions once\nagain. The exact versions get updated to avoid the issue.\n\n## Contributing\n\nContribution guide will be developed soon.\n\nFormat the code with:\n\n```bash\nisort -m 3 --fgw 3 --tc .\nblack -t py36 .\n```\n\n## References\n\nThis software is part of contribution made by [Data Mining Group of Silesian\nUniversity of Technology](http://www.zaed.polsl.pl/), rest of which is\npublished [here](https://github.com/ZAEDPolSl).\n\n- [Mrukwa, G. and Polanska, J., 2020. DiviK: Divisive intelligent K-means for\nhands-free unsupervised clustering in biological big data. *arXiv preprint\narXiv:2009.10706.*][1]\n\n[1]: https://arxiv.org/abs/2009.10706\n',
    'author': 'Grzegorz Mrukwa',
    'author_email': 'g.mrukwa@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gmrukwa/divik',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
