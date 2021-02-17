# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prts', 'prts.base', 'prts.time_series_metrics']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.4,<2.0.0']

setup_kwargs = {
    'name': 'prts',
    'version': '1.0.0.3',
    'description': '',
    'long_description': '# Precision and Recall for Time Series\n\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n![Python package](https://github.com/CompML/PRTS/workflows/Python%20package/badge.svg?branch=main)\n[![PyPI version](https://badge.fury.io/py/prts.svg)](https://badge.fury.io/py/prts)\n\nUnofficial python implementation of [Precision and Recall for Time Series](https://papers.nips.cc/paper/2018/file/8f468c873a32bb0619eaeb2050ba45d1-Paper.pdf).\n\n>Classical anomaly detection is principally concerned with point-based anomalies, those anomalies that occur at a single point in time. Yet, many real-world anomalies are range-based, meaning they occur over a period of time. Motivated by this observation, we present a new mathematical model to evaluate the accuracy of time series classification algorithms. Our model expands the well-known Precision and Recall metrics to measure ranges, while simultaneously enabling customization support for domain-specific preferences.\n\nThis is the open source software released by [Computational Mathematics Laboratory](https://sites.google.com/view/compml/). It is available for download on [PyPI](https://pypi.org/project/prts/).\n\n## Installation\n\n\n### PyPI\n\nPRTS is on [PyPI](https://pypi.org/project/prts/), so you can use pip to install it.\n\n```bash\n$ pip install prts\n```\n\n### from github\nYou can also use the following command to install.\n\n```bash\n$ git clone https://github.com/CompML/PRTS.git\n$ cd PRTS\n$ make install  # (or make develop)\n```\n\n## Usage\n\n```python\nfrom prts import ts_precision, ts_recall\n\n\n# calculate time series precision score\nprecision_flat = ts_precision(real, pred, alpha=0.0, cardinality="reciprocal", bias="flat")\nprecision_front = ts_precision(real, pred, alpha=0.0, cardinality="reciprocal", bias="front")\nprecision_middle = ts_precision(real, pred, alpha=0.0, cardinality="reciprocal", bias="middle")\nprecision_back = ts_precision(real, pred, alpha=0.0, cardinality="reciprocal", bias="back")\nprint("precision_flat=", precision_flat)\nprint("precision_front=", precision_front)\nprint("precision_middle=", precision_middle)\nprint("precision_back=", precision_back)\n\n# calculate time series recall score\nrecall_flat = ts_recall(real, pred, alpha=0.0, cardinality="reciprocal", bias="flat")\nrecall_front = ts_recall(real, pred, alpha=0.0, cardinality="reciprocal", bias="front")\nrecall_middle = ts_recall(real, pred, alpha=0.0, cardinality="reciprocal", bias="middle")\nrecall_back = ts_recall(real, pred, alpha=0.0, cardinality="reciprocal", bias="back")\nprint("recall_flat=", recall_flat)\nprint("recall_front=", recall_front)\nprint("recall_middle=", recall_middle)\nprint("recall_back=", recall_back)\n```\n\n### Parameters\n\n| Parameter   | Description                                                          | Type   |\n|-------------|----------------------------------------------------------------------|--------|\n| alpha       | Relative importance of existence reward (0 ≤ alpha ≤ 1).             | float  |\n| cardinality | Cardinality type. This should be "one", "reciprocal" or "udf_gamma"  | string |\n| bias        | Positional bias. This should be "flat", "front", "middle", or "back" | string |\n\n## Examples\n\nWe provide a simple example code.\nBy the following command you can run the example code for the toy dataset and visualize the metrics.\n\n```bash\n$ python3 examples/precision_recall_for_time_series.py\n```\n\n![example output](./examples/example.png)\n\n## Tests\n\nYou can run all the test codes as follows:\n\n```bash\n$ make test\n```\n\n## References\n* Tatbul, Nesime, Tae Jun Lee, Stan Zdonik, Mejbah Alam, and Justin Gottschlich. 2018. “Precision and Recall for Time Series.” In Advances in Neural Information Processing Systems, edited by S. Bengio, H. Wallach, H. Larochelle, K. Grauman, N. Cesa-Bianchi, and R. Garnett, 31:1920–30. Curran Associates, Inc.\n\n## LICENSE\nThis repository is Apache-style licensed, as found in the [LICENSE file](LICENSE).\n\n## Citation\n\n```bibtex\n@software{https://doi.org/10.5281/zenodo.4428056,\n  doi = {10.5281/ZENODO.4428056},\n  url = {https://zenodo.org/record/4428056},\n  author = {Ryohei Izawa, Ryosuke Sato, Masanari Kimura},\n  title = {PRTS: Python Library for Time Series Metrics},\n  publisher = {Zenodo},\n  year = {2021},\n  copyright = {Open Access}\n}\n\n```\n',
    'author': 'Ryohei Izawa',
    'author_email': 'rizawa@ridge-i.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
