# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['SwissKnife',
 'SwissKnife.avro',
 'SwissKnife.calendar',
 'SwissKnife.gcloud',
 'SwissKnife.info']

package_data = \
{'': ['*']}

install_requires = \
['coverage>=4.5,<5.0', 'nose>=1.3,<2.0']

extras_require = \
{'all': ['fastavro>=0.22,<0.23',
         'google-cloud-storage>=1.23,<2.0',
         'backoff>=1.10,<2.0'],
 'avro': ['fastavro>=0.22,<0.23'],
 'gcloud': ['google-cloud-storage>=1.23,<2.0', 'backoff>=1.10,<2.0']}

setup_kwargs = {
    'name': 'udaswissknife',
    'version': '0.11.0',
    'description': 'Utils and common libraries for Python',
    'long_description': "[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](code_of_conduct.md)\n\n\n# SwissKnife\n\nHey! Welcome to `SwissKnife`, a set of tools and functionalities built by the Data Engineering team at [@uDATech](https://twitter.com/uDAtech).\n\nThis library is born from an urge of having a common repo to gather some functions that are widely used accross our tools.\n\nSuggestions and contributions are more than welcome, always respecting our [Code of Conduct](./CODE_OF_CONDUCT.md).\n\n## Installation guide\n\nThis repo is available to download via [PyPI](https://pypi.org/project/UDASwissKnife/) and it has different sets of functionalities that can be independently installed:\n\n- **Basic** set:\n  + Packages included:\n    + `info`\n  ```bash\n  pip install UDASwissKnife\n  ```\n\n- **Extended** set:\n  + Packages included:\n    + `avro`\n    + `gcloud`\n  ```bash\n  pip install UDASwissKnife[avro,gcloud]\n  ```\n\n- **Complete** set:\n  + Includes both _Basic_ and _Extended_ sets\n  ```bash\n  pip install UDASwissKnife[all]\n  ```\n\n## Using the modules\n\n### `info`\nThe main goal of this module is to identify the environment in which we are currently working. This is done thanks to an environment variable `$ENV` which contains the name of the working environment. The accepted case insensitive values of this working environment are:\n\nThe object `SwissKnife.info.CURRENT_ENVIRONMENT`, which is of type `ExecutionEnvironment`, an enum that contains the following entries:\n\n- `PRO`\n- `PRE`\n- `TEST`\n- `DEV` (default)\n\nThen, it's possible to know the working environment using a set of methods which return a boolean indicating whether we are in that environment or not:\n\n- `is_pro()`\n- `is_pre()`\n- `is_test()`\n- `is_dev()`\n\nIt's also possible to obtain the working environment using object `SwissKnife.info.CURRENT_ENVIRONMENT`.\n\n## Why is there a Dockerfile?\n\nThe one and only purpose of the `Dockerfile` is to execute the tests defined in the project. By building and running the Docker image, tests results will be printed in the terminal. If it's needed to save the result in a file, run:\n\n```bash\nsudo docker run swissknife:latest > nosetests.xml\n```",
    'author': 'UDARealState Data engineering Team',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/urbandataanalytics/SwissKnife',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
