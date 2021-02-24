# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['skgrf', 'skgrf.ensemble']

package_data = \
{'': ['*']}

install_requires = \
['scikit-learn']

setup_kwargs = {
    'name': 'skgrf',
    'version': '0.0.0',
    'description': 'python bindings for C++ generalized random forests (grf)',
    'long_description': "skgrf\n=====\n\n|actions| |travis| |rtd| |pypi| |pyversions|\n\n.. |actions| image:: https://github.com/crflynn/skgrf/workflows/build/badge.svg\n    :target: https://github.com/crflynn/skgrf/actions\n\n.. |travis| image:: https://img.shields.io/travis/crflynn/skgrf-wheels/main.svg?logo=travis&label=wheels\n    :target: https://travis-ci.org/crflynn/skgrf-wheels\n\n.. |rtd| image:: https://img.shields.io/readthedocs/skgrf.svg\n    :target: http://skgrf.readthedocs.io/en/latest/\n\n.. |pypi| image:: https://img.shields.io/pypi/v/skgrf.svg\n    :target: https://pypi.python.org/pypi/skgrf\n\n.. |pyversions| image:: https://img.shields.io/pypi/pyversions/skgrf.svg\n    :target: https://pypi.python.org/pypi/skgrf\n\n``skgrf`` provides `scikit-learn <https://scikit-learn.org/stable/index.html>`__ compatible Python bindings to the C++ random forest implementation, `grf <https://github.com/grf-labs/grf>`__, using `Cython <https://cython.readthedocs.io/en/latest/>`__.\n\nThe latest release of ``skgrf`` uses version `1.2.0 <https://github.com/grf-labs/grf/releases/tag/v1.2.0>`__ of ``grf``.\n\n``skgrf`` is still in development. Please create issues for any discrepancies or errors. PRs welcome.\n\n\nInstallation\n------------\n\n``skgrf`` is available on `pypi <https://pypi.org/project/skgrf>`__ and can be installed via pip:\n\n.. code-block:: bash\n\n    pip install skgrf\n\nEstimators\n----------\n\n* GRFBoostedRegressor\n* GRFCausalRegressor\n* GRFInstrumentalRegressor\n* GRFLocalLinearRegressor\n* GRFQuantileRegressor\n* GRFRegressor\n* GRFSurvival\n\nUsage\n-----\n\nGRFRegressor\n~~~~~~~~~~~~\n\nThe ``GRFRegressor`` predictor uses ``grf``'s RegressionPredictionStrategy class.\n\n.. code-block:: python\n\n    from sklearn.datasets import load_boston\n    from sklearn.model_selection import train_test_split\n    from skgrf.ensemble import GRFRegressor\n    \n    X, y = load_boston(return_X_y=True)\n    X_train, X_test, y_train, y_test = train_test_split(X, y)\n    \n    rfr = GRFRegressor()\n    rfr.fit(X_train, y_train)\n    \n    predictions = rfr.predict(X_test)\n    print(predictions)\n    # [31.81349144 32.2734354  16.51560285 11.90284392 39.69744341 21.30367911\n    #  19.52732937 15.82126562 26.49528961 11.27220097 16.02447197 20.01224404\n    #  ...\n    #  20.70674263 17.09041289 12.89671205 20.79787926 21.18317924 25.45553279\n    #  20.82455595]\n\n\nGRFQuantileRegressor\n~~~~~~~~~~~~~~~~~~~~\n\nThe ``GRFQuantileRegressor`` predictor uses ``grf``'s QuantilePredictionStrategy class.\n\n.. code-block:: python\n\n    from sklearn.datasets import load_boston\n    from sklearn.model_selection import train_test_split\n    from skgrf.ensemble import GRFQuantileRegressor\n    \n    X, y = load_boston(return_X_y=True)\n    X_train, X_test, y_train, y_test = train_test_split(X, y)\n    \n    gqr = GRFQuantileRegressor(quantiles=[0.1, 0.9])\n    gqr.fit(X_train, y_train)\n    \n    predictions = gqr.predict(X_test)\n    print(predictions)\n    # [[21.9 50. ]\n    # [ 8.5 24.5]\n    # ...\n    # [ 8.4 18.6]\n    # [ 8.1 20. ]]\n\nLicense\n-------\n\n``skgrf`` is licensed under `GPLv3 <https://github.com/crflynn/skgrf/blob/main/LICENSE.txt>`__.\n\nDevelopment\n-----------\n\nTo develop locally, it is recommended to have ``asdf``, ``make`` and a C++ compiler already installed. After cloning, run ``make setup``. This will setup the grf submodule, install python and poetry from ``.tool-versions``, install dependencies using poetry, copy the grf source code into skgrf, and then build and install skgrf in the local virtualenv.\n\nTo format code, run ``make fmt``. This will run isort and black against the .py files.\n\nTo run tests and inspect coverage, run ``make test``.\n\nTo rebuild in place after making changes, run ``make build``.\n\nTo create python package artifacts, run ``make dist``.\n\nTo build and view documentation, run ``make docs``.\n",
    'author': 'flynn',
    'author_email': 'crf204@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/crflynn/skgrf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
