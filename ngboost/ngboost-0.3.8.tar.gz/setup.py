# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ngboost', 'ngboost.distns']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata>=3.4.0,<4.0.0',
 'lifelines>=0.25,<0.29',
 'numpy>=1.17,<2.0',
 'scikit-learn>=0.21,<0.24',
 'scipy>=1.3,<2.0',
 'tqdm>=4.4,<5.0']

setup_kwargs = {
    'name': 'ngboost',
    'version': '0.3.8',
    'description': 'Library for probabilistic predictions via gradient boosting.',
    'long_description': '# NGBoost: Natural Gradient Boosting for Probabilistic Prediction\n\n![Python package](https://github.com/stanfordmlgroup/ngboost/workflows/Python%20package/badge.svg)\n[![Github License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nngboost is a Python library that implements Natural Gradient Boosting, as described in ["NGBoost: Natural Gradient Boosting for Probabilistic Prediction"](https://stanfordmlgroup.github.io/projects/ngboost/). It is built on top of [Scikit-Learn](https://scikit-learn.org/stable/), and is designed to be scalable and modular with respect to choice of proper scoring rule, distribution, and base learner. A didactic introduction to the methodology underlying NGBoost is available in this [slide deck](https://drive.google.com/file/d/183BWFAdFms81MKy6hSku8qI97OwS_JH_/view?usp=sharing).\n\n## Installation\n\n```sh\nvia pip\n\npip install --upgrade ngboost\n\nvia conda-forge\n\nconda install -c conda-forge ngboost\n```\n\n## Usage\n\nProbabilistic regression example on the Boston housing dataset:\n\n```python\nfrom ngboost import NGBRegressor\n\nfrom sklearn.datasets import load_boston\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import mean_squared_error\n\nX, Y = load_boston(True)\nX_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)\n\nngb = NGBRegressor().fit(X_train, Y_train)\nY_preds = ngb.predict(X_test)\nY_dists = ngb.pred_dist(X_test)\n\n# test Mean Squared Error\ntest_MSE = mean_squared_error(Y_preds, Y_test)\nprint(\'Test MSE\', test_MSE)\n\n# test Negative Log Likelihood\ntest_NLL = -Y_dists.logpdf(Y_test).mean()\nprint(\'Test NLL\', test_NLL)\n```\n\nDetails on available distributions, scoring rules, learners, tuning, and model interpretation are available in our [user guide](https://stanfordmlgroup.github.io/ngboost/intro.html), which also includes numerous usage examples and information on how to add new distributions or scores to NGBoost.\n\n## License\n\n[Apache License 2.0](https://github.com/stanfordmlgroup/ngboost/blob/master/LICENSE).\n\n## Reference\n\nTony Duan, Anand Avati, Daisy Yi Ding, Khanh K. Thai, Sanjay Basu, Andrew Y. Ng, Alejandro Schuler. 2019.\nNGBoost: Natural Gradient Boosting for Probabilistic Prediction.\n[arXiv](https://arxiv.org/abs/1910.03225)\n',
    'author': 'Stanford ML Group',
    'author_email': 'avati@cs.stanford.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stanfordmlgroup/ngboost',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
