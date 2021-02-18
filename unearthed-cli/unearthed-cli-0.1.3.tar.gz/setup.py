# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unearthed',
 'unearthed.cli',
 'unearthed.cli.commands',
 'unearthed.core.auth',
 'unearthed.core.models',
 'unearthed.logs']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=1.7.1,<2.0.0',
 'boto3>=1.16.39,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'cognitojwt>=1.2.2,<2.0.0',
 'colorama>=0.4.4,<0.5.0',
 'docker>=4.4.0,<5.0.0',
 'outdated>=0.2.0,<0.3.0',
 'pycognito>=0.1.4,<0.2.0',
 'requests>=2.25.1,<3.0.0',
 'tqdm>=4.54.1,<5.0.0']

entry_points = \
{'console_scripts': ['unearthed = unearthed.cli:main']}

setup_kwargs = {
    'name': 'unearthed-cli',
    'version': '0.1.3',
    'description': 'Unearthed CLI Tool',
    'long_description': '# Crowd ML CLI\n\nThis is the command line tool for [Unearthed Solutions CrowdML challenges](https://unearthed.solutions/).\n\nIt is designed to make model validation and submission straightforward.\n\nPlease see the [Unearthed Solutions Terms and Conditions](https://unearthed.solutions/u/terms)\n\n# Commands\n\n## `unearthed login`\n\nPrompts the user for their innovator portal login and stores the tokens. You must be logged in to run other commands.\n\n## `unearthed new`\n\nThis command asks the user which challenge they wish to download and unpack the model template for. The template will be unpacked in a named folder inside the current directory. A custom path can be specified with `unearthed new /path/to/dir/`\n\n## `unearthed submit`\n\nThis will bundle the source code in a Docker container and then submit the code to the submission pipeline. The user is provided a link to the submission tracker, which will auto-popup in their browser, so they can track the progress and logs of their submission.\n\nYou can disable the tracker from opening in the browser by specifying `unearthed submit --no-tracker`\n\n## `unearthed tracker`\n\nWill open the tracker for the last submission that was made.\n\n## `unearthed preprocess`\n\nThis command will run the preprocess code in a Docker container similar to how it will execute in the submission pipeline. It can be used to validate the preprocessing code is working before submitting.\n\n### `unearthed train`\n\nThis command will train a model, including calling the preprocessing code, in a Docker container similar to how it will execute in the submission pipeline. It can be used to validate the training code is working before submitting.\n\n### `unearthed predict`\n\nThis command will simulate generating predictions on the public dataset so that the predictions can be inspected locally before submitting.\n\n### `unearhted score`\n\nThis command will run the scoring function to generate a score against the public dataset. It can be used to check the score against the public dataset before submitting.\n',
    'author': 'Unearthed Solutions',
    'author_email': 'info@unearthed.solutions',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://unearthed.solutions',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
