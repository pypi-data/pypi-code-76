# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['batchdist',
 'batchdist.examples',
 'batchdist.examples.external',
 'batchdist.src']

package_data = \
{'': ['*']}

install_requires = \
['torch>=1.6.0,<2.0.0']

setup_kwargs = {
    'name': 'batchdist',
    'version': '0.1.3',
    'description': 'A small pytorch package for efficiently running pair-wise operations such as distances on the batch-level.',
    'long_description': '# batchdist  \n\nThis is a small PyTorch-based package which allows for efficient batched operations, e.g. for computing distances without having to slowly loop over all instance pairs of a batch of data.\n\nAfter having encountered mulitple instances of torch modules/methods promising to handling batches while only returning a vector of pairwise results (see example below) instead of the full matrix, this package serves as a tool to wrap such methods in order to return full matrices (e.g. distance matrices) using fast, batched operations (without loops). \n\n## Example  \n\nFirst, let\'s define a custom distance function that only computes pair-wise distances for batches, so two batches of each 10 samples are \nconverted to a distance vector of shape (10,).\n```python  \n>>> def dummy_distance(x,y):\n        """\n        This is a dummy distance d which allows for a batch dimension \n        (say with n instances in a batch), but does not return the full \n        n x n distance matrix but only a n-dimensional vector of the \n        pair-wise distances d(x_i,y_i) for all i in (1,...,n). \n        """\n        x_ = x.sum(axis=[1,2])\n        y_ = y.sum(axis=[1,2])\n        return x_ + y_\n\n# batchdist wraps a torch module around this callable to compute \n# the full n x n matrix with batched operations (no loops). \n\n>>> import batchdist as bd\n>>> batched = bd.BatchDistance(dummy_distance)\n\n# generate data (two batches of 256 samples of dimension [4,3])\n\n>>> x1 = torch.rand(256,4,3)\n>>> x2 = torch.rand(256,4,3)\n\n>>> out1 = batched(x1, x2) # distance matrix of shape [256,256]\n```\n \nFor more details, consult the included examples.\n\n## Installation \n\nWith poetry:  \n```$ poetry add batchdist```  \n \nWith pip:  \n```$ pip install batchdist```   \n\n',
    'author': 'Michael Moor',
    'author_email': 'michael.moor@bsse.ethz.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mi92/batchdist',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
