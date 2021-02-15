# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gen3utils',
 'gen3utils.deployment_changes',
 'gen3utils.etl',
 'gen3utils.manifest',
 'gen3utils.s3log']

package_data = \
{'': ['*']}

install_requires = \
['cdislogging>=1.0.0,<1.1.0',
 'click',
 'dictionaryutils>=3.0.0,<3.1.0',
 'gen3datamodel>=3.0.0,<3.1.0',
 'gen3dictionary>=2.0.1,<2.1.0',
 'gen3git>=0.3.3,<0.4.0',
 'packaging>=20.0,<20.1',
 'psqlgraph>=3.0.0,<3.1.0',
 'pyyaml>=5.1,<5.2',
 'six>=1.12.0,<1.13.0']

extras_require = \
{':extra == "s3log"': ['aiobotocore>=1.2.0,<2.0.0']}

entry_points = \
{'console_scripts': ['gen3utils = gen3utils.main:main']}

setup_kwargs = {
    'name': 'gen3utils',
    'version': '0.5.8',
    'description': 'Gen3 Library Template',
    'long_description': '# gen3utils\n\nUtils for Gen3 commons management\n\n## manifest.json validation\n\nValidate one or more `manifest.json` files:\n```\npip install gen3utils\ngen3utils validate-manifest cdis-manifest/*/manifest.json\n```\n\nThe validation settings can be updated by modifying [this file](gen3utils/manifest/validation_config.yaml).\n\n## etlMapping.yaml validation\n\nValidate an `etlMapping.yaml` file against the dictionary URL specified in a `manifest.json` file:\n```\npip install gen3utils\ngen3utils validate-etl-mapping etlMapping.yaml manifest.json\n```\n\n## Comment on a PR with any deployment changes when updating manifest services\n\nThe command requires the name of the repository, the pull request number and **a `GITHUB_TOKEN` environment variable** containing a token with read and write access to the repository. It also comments a warning if a service is pinned on a branch.\n```\npip install gen3utils\ngen3utils post-deployment-changes <username>/<repository> <pull request number>\n```\n\n## Running tests locally\n\n```\npoetry install -vv\npoetry run pytest -vv ./tests\n```\n',
    'author': 'CTDS UChicago',
    'author_email': 'cdis@uchicago.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/uc-cdis/gen3utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<3.7',
}


setup(**setup_kwargs)
