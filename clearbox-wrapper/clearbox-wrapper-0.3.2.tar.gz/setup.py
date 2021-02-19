# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clearbox_wrapper',
 'clearbox_wrapper.data_preparation',
 'clearbox_wrapper.exceptions',
 'clearbox_wrapper.keras',
 'clearbox_wrapper.model',
 'clearbox_wrapper.preprocessing',
 'clearbox_wrapper.pyfunc',
 'clearbox_wrapper.pytorch',
 'clearbox_wrapper.schema',
 'clearbox_wrapper.signature',
 'clearbox_wrapper.sklearn',
 'clearbox_wrapper.utils',
 'clearbox_wrapper.wrapper',
 'clearbox_wrapper.xgboost']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'cloudpickle>=1.6.0,<2.0.0',
 'loguru>=0.5.3,<0.6.0',
 'numpy>=1.19.0,<2.0.0',
 'pandas>=1,<2']

setup_kwargs = {
    'name': 'clearbox-wrapper',
    'version': '0.3.2',
    'description': 'An agnostic wrapper for the most common frameworks of ML models.',
    'long_description': '[![Tests](https://github.com/Clearbox-AI/clearbox-wrapper/workflows/Tests/badge.svg)](https://github.com/Clearbox-AI/clearbox-wrapper/actions?workflow=Tests)\n\n[![PyPI](https://img.shields.io/pypi/v/clearbox-wrapper.svg)](https://pypi.org/project/clearbox-wrapper/)\n\n# Clearbox AI Wrapper\n\nClearbox AI Wrapper is a Python library to package and save a Machine Learning model built with common ML/DL frameworks. It is designed to wrap models trained on strutured data. It includes optional pre-processing and data cleaning functions which can be used to build ready-to-production pipelines.\n\n## Main Features\n\nThe wrapper is largely based on [mlflow](https://github.com/mlflow/mlflow) and its [standard format](https://mlflow.org/docs/latest/models.html). It adds the possibility to package, together with the fitted model, pre-processing and data cleaning functions in order to create a production-ready pipeline able to receive new data, pre-process them and makes predictions. The resulting wrapped model/pipeline is saved as a zipped folder.\n\nThe library is designed to automatically detect the model framework and its version adding this information to the requirements saved into the final folder. Additional dependencies (e.g. libraries used in pre-processing or data cleaning) can also be added as a list parameter if necessary.\n\nThe resulting wrapped folder can be loaded via the Wrapper and the model will be ready to take input through the `predict` methods. The optional pre-processing and data cleaning functions, if present, can be loaded as separate functions as well.\n\n**IMPORTANT**: The `predict` method of the wrapped model outputs class probabilities by default (if the corresponding method is present in the original model). If a `predict_proba` method is not present in the wrapped model (e.g. regression problems or models that output probabilities by default), the wrapper will use the `predict` method instead.\n\n## Pre-processing\n\nTypically, data are pre-processed before being fed into the model. It is almost always necessary to transform (e.g. scaling, binarizing,...) raw data values into a representation that is more suitable for the downstream model. Most kinds of ML models take only numeric data as input, so we must at least encode the non-numeric data, if any.\n\nPre-processing is usually written and performed separately, before building and training the model. We fit some transformers, transform the whole dataset(s) and train the model on the processed data. If the model goes into production, we need to ship the pre-processing as well. New raw data must be processed on the same way the training dataset was.\n\nWith Clearbox AI Wrapper it\'s possible to wrap and save the pre-processing along with the model so to have a pipeline Processing+Model ready to take raw data, pre-process them and make predictions.\n\nAll the pre-processing code **must be wrapped in a single function** so it can be passed as a parameter to the `save_model` method. You can use your own custom code for the preprocessing, just remember to wrap all of it in a single function, save it along with the model and add any extra dependencies.\n\n**IMPORTANT**: If the pre-processing includes any kind of fitting on the training dataset (e.g. Scikit Learn transformers), it must be performed outside the final pre-processing function to save. Fit the transformer(s) outside the function and put only the `transform` method inside it. Furthermore, if the entire pre-processing is performed with a single Scikit-Learn transformer, you can directly pass it (fitted) to the `save_model` method.\n\n\n## Data Cleaning (advanced usage)\n\nFor a complex task, a single-step pre-processing could be not enough. Raw data initially collected could be very noisy, contain useless columns or splitted into different dataframes/tables sources. A first data processing is usually performed even before considering any kind of model to feed the data in. The entire dataset is cleaned and the following additional processing and the model are built considering only the cleaned data. But this is not always the case. Sometimes, this situation still applies for data fed in real time to a model in production.\n\nWe believe that a two-step data processing is required to deal with this situation. We refer to the first additional step by the term **Data Cleaning**. With Clearbox AI Wrapper it\'s possible to wrap a data cleaning step as well, in order to save a final Data Cleaning + Pre-processing + Model pipeline ready to takes input.\n\nAll the data cleaning code **must be wrapped in a single function** so it can be passed as a parameter to the `save_model` method. The same considerations wrote above for the pre-processing step still apply for data cleaning.\n\n### Data Cleaning vs. Pre-processing\n\nIt is not always clear which are the differences between pre-processing and data cleaning. It\'s not easy to understand where data cleaning ends and pre-processing begins. There are no conditions that apply in any case, but in general you should build the data cleaning step working only with the dataset, without considering the model your data will be fed into. Any kind of operation is allowed, but often cleaning the raw data includes removing or normalizing some columns, replacing values, add a column based on other column values,... After this step, no matter what kind of transformation the data have been through, they should still be readable and understandable by a human user.\n\nThe pre-processing step, on the contrary, should be considered closely tied with the downstream ML model and adapted to its particular "needs". Typically processed data by this second step are only numeric and non necessarily understandable by a human.\n\n## Supported ML frameworks\n\n* Scikit-Learn\n* XGBoost\n* Keras\n* Pytorch\n## Installation\n\nInstall the latest relased version on the [Python Package Index (PyPI)](https://pypi.org/project/clearbox-wrapper/) with\n\n```shell\npip install clearbox-wrapper\n```\n\n## Quickstart\n\nYou can import the Wrapper with\n\n```python\nimport clearbox_wrapper as cbw\n```\n\nThe following lines show how to wrap and save a simple Scikit-Learn model without pre-processing or data cleaning:\n\n```python\nmodel = DecisionTreeClassifier(max_depth=4, random_state=42)\nmodel.fit(X_train, y_train)\ncbw.save_model(\'wrapped_model_path\', model)\n```\n\nThis is a simple extract from [this notebook](https://github.com/Clearbox-AI/clearbox-wrapper/blob/master/examples/1_iris_sklearn/1_Clearbox_Wrapper_Iris_Scikit.ipynb). Please see the following examples for a better understing about the usage.\n\n## Examples\n\n* [Scikit Learn Decision Tree on Iris Dataset](https://github.com/Clearbox-AI/clearbox-wrapper/blob/master/examples/1_iris_sklearn/1_Clearbox_Wrapper_Iris_Scikit.ipynb) (No preprocessing, No data cleaning)\n* [XGBoost Model on Lending Club Loans Dataset](https://github.com/Clearbox-AI/clearbox-wrapper/blob/master/examples/2_loans_preprocessing_xgboost/2_Clearbox_Wrapper_Loans_Xgboost.ipynb) (Preprocessing, No data cleaning)\n* [Pytorch Network on Boston Housing Dataset](https://github.com/Clearbox-AI/clearbox-wrapper/blob/master/examples/3_boston_preprocessing_pytorch/3_Clearbox_Wrapper_Boston_Pytorch.ipynb) (Preprocessing, No data cleaning)\n* [Keras Network on UCI Adult Dataset](https://github.com/Clearbox-AI/clearbox-wrapper/blob/master/examples/4_adult_data_cleaning_preprocessing_keras/4_Clearbox_Wrapper_Adult_Keras.ipynb) (Preprocessing and data cleaning)\n* [Pytorch Network on Diabetes Hospital Readmissions](https://github.com/Clearbox-AI/clearbox-wrapper/blob/master/examples/5_hospital_preprocessing_pytorch/4_Clearbox_Wrapper_Hospital_Pytorch.ipynb) (Preprocessing and data cleaning)\n\n## License\n\n[Apache License 2.0](https://github.com/Clearbox-AI/clearbox-wrapper/blob/master/LICENSE)\n',
    'author': 'Clearbox AI',
    'author_email': 'info@clearbox.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://clearbox.ai',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
