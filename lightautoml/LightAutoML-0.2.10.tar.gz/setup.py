# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lightautoml',
 'lightautoml.addons',
 'lightautoml.addons.utilization',
 'lightautoml.automl',
 'lightautoml.automl.presets',
 'lightautoml.dataset',
 'lightautoml.image',
 'lightautoml.ml_algo',
 'lightautoml.ml_algo.torch_based',
 'lightautoml.ml_algo.tuning',
 'lightautoml.pipelines',
 'lightautoml.pipelines.features',
 'lightautoml.pipelines.ml',
 'lightautoml.pipelines.selection',
 'lightautoml.reader',
 'lightautoml.report',
 'lightautoml.tasks',
 'lightautoml.tasks.losses',
 'lightautoml.text',
 'lightautoml.transformers',
 'lightautoml.utils',
 'lightautoml.validation']

package_data = \
{'': ['*'],
 'lightautoml.automl.presets': ['tabular_configs/*'],
 'lightautoml.report': ['lama_report_templates/*']}

install_requires = \
['albumentations',
 'autowoe>=1.2',
 'catboost',
 'cmaes',
 'efficientnet-pytorch',
 'gensim',
 'holidays',
 'jinja2',
 'joblib',
 'json2html',
 'lightgbm>=2.3,<3.0',
 'log-calls',
 'networkx',
 'nltk',
 'numpy',
 'opencv-python',
 'optuna',
 'pandas>=1',
 'poetry-core>=1.0.0,<2.0.0',
 'pywavelets',
 'pyyaml',
 'scikit-image',
 'scikit-learn>=0.22',
 'scipy',
 'seaborn',
 'torch>=1.6',
 'torchvision',
 'tqdm',
 'transformers>=4',
 'webencodings']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

setup_kwargs = {
    'name': 'lightautoml',
    'version': '0.2.10',
    'description': 'Fast and customizable framework for automatic ML model creation (AutoML)',
    'long_description': '# LightAutoML - automatic model creation framework\n\n[![Slack](https://lightautoml-slack.herokuapp.com/badge.svg)](https://lightautoml-slack.herokuapp.com)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/lightautoml?color=green&label=PyPI%20downloads&logo=pypi&logoColor=orange&style=plastic)\n![Read the Docs](https://img.shields.io/readthedocs/lightautoml?style=plastic)\n\nLightAutoML project from Sberbank AI Lab AutoML group is the framework for automatic classification and regression model creation.\n\nCurrent available tasks to solve:\n- binary classification\n- multiclass classification\n- regression\n\nCurrently we work with datasets, where **each row is an object with its specific features and target**. Multitable datasets and sequences are now under contruction :)\n\n**Note**: for automatic creation of interpretable models we use [`AutoWoE`](https://github.com/sberbank-ai-lab/AutoMLWhitebox) library made by our group as well.\n\n**Authors**: Ryzhkov Alexander, Vakhrushev Anton, Simakov Dmitry, Bunakov Vasilii, Damdinov Rinchin, Shvets Pavel, Kirilin Alexander\n\n**LightAutoML video guides**:\n- [LightAutoML webinar for Sberloga community](https://www.youtube.com/watch?v=ci8uqgWFJGg) (Ryzhkov Alexander, Simakov Dmitry)\n- [LightAutoML framework general overview, benchmarks and advantages for business](https://vimeo.com/485383651) (Ryzhkov Alexander)\n- [LightAutoML practical guide - ML pipeline presets overview](https://vimeo.com/487166940) (Simakov Dmitry)\n\nSee the [Documentation of LightAutoML](https://lightautoml.readthedocs.io/).\n\n*******\n# Installation\n### Installation via pip from PyPI\nTo install LightAutoML framework on your machine:\n```bash \npip install -U lightautoml\n```\n### Installation from sources with virtual environment creation\nIf you want to create a specific virtual environment for LightAutoML, you need to install  `python3-venv` system package and run the following command, which creates `lama_venv` virtual env with LightAutoML inside:\n```bash \nbash build_package.sh\n```\nTo check this variant of installation and run all the demo scripts, use the command below:\n```bash \nbash test_package.sh\n```\n*******\n# Docs generation\nTo generate documentation for LightAutoML framework, you can use command below (it uses virtual env created on installation step from sources):\n```bash \nbash build_docs.sh\n```\n\nBuilded official documentation for LightAutoML is available [`here`](https://lightautoml.readthedocs.io/en/latest/).\n*******\n# Usage examples\n\nTo find out how to work with LightAutoML, we have several tutorials:\n1. `Tutorial_1. Create your own pipeline.ipynb` - shows how to create your own pipeline from specified blocks: pipelines for feature generation and feature selection, ML algorithms, hyperparameter optimization etc.\n2. `Tutorial_2. AutoML pipeline preset.ipynb` - shows how to use LightAutoML presets (both standalone and time utilized variants) for solving ML tasks on tabular data. Using presets you can solve binary classification, multiclass classification and regression tasks, changing the first argument in Task.\n3. `Tutorial_3. Multiclass task.ipynb` - shows how to build ML pipeline for multiclass ML task by hand\n\nEach tutorial has the step to enable Profiler and completes with Profiler run, which generates distribution for each function call time and shows it in interactive HTML report: the report show full time of run on its top and interactive tree of calls with percent of total time spent by the specific subtree.\n\n**Important 1**: for production you have no need to use profiler (which increase work time and memory consomption), so please do not turn it on - it is in off state by default\n\n**Important 2**: to take a look at this report after the run, please comment last line of demo with report deletion command. \n\nFor more examples, in `tests` folder you can find different scenarios of LightAutoML usage:\n1. `demo0.py` - building ML pipeline from blocks and fit + predict the pipeline itself.\n2. `demo1.py` - several ML pipelines creation (using importances based cutoff feature selector) to build 2 level stacking using AutoML class\n3. `demo2.py` - several ML pipelines creation (using iteartive feature selection algorithm) to build 2 level stacking using AutoML class\n4. `demo3.py` - several ML pipelines creation (using combination of cutoff and iterative FS algos) to build 2 level stacking using AutoML class\n5. `demo4.py` - creation of classification and regression tasks for AutoML with loss and evaluation metric setup\n6. `demo5.py` - 2 level stacking using AutoML class with different algos on first level including LGBM, Linear and LinearL1\n7. `demo6.py` - AutoML with nested CV usage\n8. `demo7.py` - AutoML preset usage for tabular datasets (predefined structure of AutoML pipeline and simple interface for users without building from blocks)\n9. `demo8.py` - creation pipelines from blocks to build AutoML, solving multiclass classification task\n10. `demo9.py` - AutoML time utilization preset usage for tabular datasets (predefined structure of AutoML pipeline and simple interface for users without building from blocks)\n11. `demo10.py` - creation pipelines from blocks (including CatBoost) to build AutoML , solving multiclass classification task\n12. `demo11.py` - AutoML NLP preset usage for tabular datasets with text columns\n13. `demo12.py` - AutoML tabular preset usage with custom validation scheme and multiprocessed inference\n\n\n******\n# Contributing to LightAutoML\n\nIf you are interested in contributing to LightAutoML, please read the [Contributing Guide](CONTRIBUTING.md) to get started.\n\n\n*******\n# Questions / Issues / Suggestions \n\nWrite a message to us:\n- Alexander Ryzhkov (_email_: AMRyzhkov@sberbank.ru, _telegram_: @RyzhkovAlex)\n- Anton Vakhrushev (_email_: AGVakhrushev@sberbank.ru)\n\n\n',
    'author': 'Alexander Ryzhkov',
    'author_email': 'AMRyzhkov@sberbank.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://lightautoml.readthedocs.io/en/latest/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
