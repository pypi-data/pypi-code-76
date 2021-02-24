# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datasetinsights',
 'datasetinsights.commands',
 'datasetinsights.datasets',
 'datasetinsights.datasets.dummy',
 'datasetinsights.datasets.protos',
 'datasetinsights.datasets.unity_perception',
 'datasetinsights.estimators',
 'datasetinsights.evaluation_metrics',
 'datasetinsights.io',
 'datasetinsights.io.downloader',
 'datasetinsights.io.tracker',
 'datasetinsights.stats',
 'datasetinsights.stats.visualization']

package_data = \
{'': ['*'],
 'datasetinsights': ['configs/*'],
 'datasetinsights.stats.visualization': ['font/*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'codetiming>=1.2.0,<2.0.0',
 'cython>=0.29.14,<0.30.0',
 'dash==1.12.0',
 'dask[complete]>=2.14.0,<3.0.0',
 'google-cloud-storage>=1.24.1,<=1.28.1',
 'jupyter>=1.0.0,<2.0.0',
 'kornia>=0.1.4,<0.2.0',
 'mlflow>=1.11.0,<2.0.0',
 'numpy>=1.17,<1.18',
 'nuscenes-devkit>=1.0.2,<1.0.3',
 'pandas>=1.0.1,<2.0.0',
 'plotly>=4.4.1,<5.0.0',
 'pycocotools>=2.0.0,<3.0.0',
 'pyquaternion>=0.9.5,<0.10.0',
 'pytorch-ignite>=0.3.0,<0.4.0',
 'tensorflow>=2.2.0,<3.0.0',
 'torch>=1.4.0,<1.5.0',
 'torchvision>=0.5,<0.6',
 'tqdm>=4.45.0,<5.0.0',
 'yacs>=0.1.6,<0.2.0']

entry_points = \
{'console_scripts': ['datasetinsights = datasetinsights.__main__:entrypoint']}

setup_kwargs = {
    'name': 'datasetinsights',
    'version': '0.2.5',
    'description': 'Synthetic dataset insights.',
    'long_description': '# Dataset Insights\n\nUnity Dataset Insights is a python package for understanding synthetic datasets.\nThis package enables users to analyze synthetic datasets generated using the [Perception SDK](https://github.com/Unity-Technologies/com.unity.perception).\n\n## Installation\n\nDataset Insights maintains a pip package for easy installation. It can work in any standard Python environment using `pip install datasetinsights` command. We support Python 3 (>= 3.7).\n\n## Getting Started\n\n### Dataset Statistics\n\nWe provide a sample [notebook](notebooks/SynthDet_Statistics.ipynb) to help you get started with dataset statistics for the [SynthDet](https://github.com/Unity-Technologies/SynthDet) project. We plan to support other sample Unity projects in the future.\n\n### Dataset Evaluation\n\nDataset evaluation provides tools to train and evaluate ML models for different datasets. You can run `download`, `train` and `evaluate` commands:\n\n[Download Dataset](https://datasetinsights.readthedocs.io/en/latest/datasetinsights.commands.html#datasetinsights-commands-download)\n\n```bash\ndatasetinsights download \\\n  --source-uri=<xxx> \\\n  --output=$HOME/data\n```\n\n[Train](https://datasetinsights.readthedocs.io/en/latest/datasetinsights.commands.html#datasetinsights-commands-train)\n\n```bash\ndatasetinsights train \\\n --config=datasetinsights/configs/faster_rcnn.yaml \\\n --train-data=$HOME/data\n```\n\n[Evaluate](https://datasetinsights.readthedocs.io/en/latest/datasetinsights.commands.html#datasetinsights-commands-evaluate)\n\n```bash\ndatasetinsights evaluate \\\n --config=datasetinsights/configs/faster_rcnn.yaml \\\n --test-data=$HOME/data\n```\n\nTo learn more, see this [tutorial](https://datasetinsights.readthedocs.io/en/latest/Evaluation_Tutorial.html).\n\n## Docker\n\nYou can use the pre-build docker image [unitytechnologies/datasetinsights](https://hub.docker.com/r/unitytechnologies/datasetinsights) to run similar commands.\n\n## Documentation\n\nYou can find the API documentation on [readthedocs](https://datasetinsights.readthedocs.io/en/latest/).\n\n## Contributing\n\nPlease let us know if you encounter a bug by filing an issue. To learn more about making a contribution to Dataset Insights, please see our Contribution [page](CONTRIBUTING.md).\n\n## License\n\nDataset Insights is licensed under the Apache License, Version 2.0. See [LICENSE](LICENCE) for the full license text.\n\n## Citation\nIf you find this package useful, consider citing it using:\n```\n@misc{datasetinsights2020,\n    title={Unity {D}ataset {I}nsights Package},\n    author={{Unity Technologies}},\n    howpublished={\\url{https://github.com/Unity-Technologies/datasetinsights}},\n    year={2020}\n}\n```\n',
    'author': 'Unity AI Perception Team',
    'author_email': 'perception@unity3d.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
