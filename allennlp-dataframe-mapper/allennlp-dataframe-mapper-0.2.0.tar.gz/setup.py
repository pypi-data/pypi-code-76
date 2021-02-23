# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['allennlp_dataframe_mapper',
 'allennlp_dataframe_mapper.common',
 'allennlp_dataframe_mapper.common.testing',
 'allennlp_dataframe_mapper.transforms']

package_data = \
{'': ['*']}

install_requires = \
['allennlp>=2.0.0,<2.1.0', 'sklearn-pandas>=2.0.2,<3.0.0']

setup_kwargs = {
    'name': 'allennlp-dataframe-mapper',
    'version': '0.2.0',
    'description': '',
    'long_description': '# AllenNLP integration for sklearn-pandas\n\n![CI](https://github.com/shunk031/allennlp-dataframe-mapper/workflows/CI/badge.svg?branch=master)\n![Release](https://github.com/shunk031/allennlp-dataframe-mapper/workflows/Release/badge.svg)\n![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8-blue?logo=python)\n[![PyPI](https://img.shields.io/pypi/v/allennlp-dataframe-mapper.svg)](https://pypi.python.org/pypi/allennlp-dataframe-mapper)\n\n`allennlp-dataframe-mapper` is a Python library that provides [AllenNLP](https://github.com/allenai/allennlp) integration for [sklearn-pandas](https://github.com/scikit-learn-contrib/sklearn-pandas).\n\n## Installation\n\nInstalling the library and dependencies is simple using `pip`.\n\n```sh\n$ pip allennlp-dataframe-mapper\n```\n\n## Example\n\nThis library enables users to specify the in a jsonnet config file.\nHere is an example of the mapper for a famous [iris dataset](https://archive.ics.uci.edu/ml/datasets/iris).\n\n### Config\n\n`allennlp-dataframe-mapper` is specified the transformations of the mapper in `jsonnet` config file like following `mapper_iris.jsonnet`:\n\n```json\n{\n    "type": "default",\n    "features": [\n        [["sepal length (cm)"], null],\n        [["sepal width (cm)"], null],\n        [["petal length (cm)"], null],\n        [["petal width (cm)"], null],\n        [["species"], [{"type": "flatten"}, {"type": "label-encoder"}]],\n    ],\n    "df_out": true,\n}\n```\n\n### Mapper\n\nThe mapper takes a param of transformations from the config file.\nWe can use the `fit_transform` shortcut to both fit the mapper and see what transformed data.\n\n```python\nfrom allennlp.common import Params\nfrom allennlp_dataframe_mapper import DataFrameMapper\n\nparams = Params.from_file("mapper_iris.jsonnet")\nmapper = DataFrameMapper.from_params(params=params)\n\nprint(mapper)\n# DataFrameMapper(df_out=True,\n#                 features=[([\'sepal length (cm)\'], None, {}),\n#                           ([\'sepal width (cm)\'], None, {}),\n#                           ([\'petal length (cm)\'], None, {}),\n#                           ([\'petal width (cm)\'], None, {}),\n#                           ([\'species\'], [FlattenTransformer(), LabelEncoder()], {})])\n\nmapper.fit_transform(df)\n```\n\n## License\n\nMIT\n',
    'author': 'Shunsuke KITADA',
    'author_email': 'shunsuke.kitada.0831@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shunk031/allennlp-dataframe-mapper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
