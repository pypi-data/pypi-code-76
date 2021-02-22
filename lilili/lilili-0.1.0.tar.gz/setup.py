# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lilili', 'lilili.apis', 'lilili.db']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=1.1.2,<2.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'SQLAlchemy>=1.3.23,<2.0.0',
 'cleo>=0.8.1,<0.9.0',
 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['lilili = lilili.cli:main']}

setup_kwargs = {
    'name': 'lilili',
    'version': '0.1.0',
    'description': 'List the Licenses of the Libraries.',
    'long_description': '# LiLiLi: List the Licenses of the Libraries\n\n[![PyPI Version](https://img.shields.io/pypi/v/lilili.svg)](https://pypi.org/pypi/lilili/)\n[![Python Versions](https://img.shields.io/pypi/pyversions/lilili.svg)](https://pypi.org/pypi/lilili/)\n[![License](https://img.shields.io/pypi/l/lilili.svg)](https://github.com/poyo46/lilili/blob/main/LICENSE)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n\nLiLiLi helps you to retrieve and audit software license information.\n\n## Installation\n\nLiLiLi is available on PyPI:\n\n```console\n$ pip install lilili\n```\n\nYou can also use [poetry](https://python-poetry.org/) to add it to a specific Python project.\n\n```console\n$ poetry add lilili\n```\n\n## Examples\n### Search for and list the licenses of libraries\n\n**Python libraries**\n\n```console\n$ pip list > pip-list.txt\n$ lilili search --yaml pip-list.txt\n```\n\nExample of `result.yml`:\n\n```yaml\n- domain: pypi\n  name: requests\n  version: 2.25.1\n  licenses:\n    - spdx_id: Apache-2.0\n      basis: API_EXACT\n      source_url: https://pypi.org/pypi/requests/2.25.1/json\n  download_url: https://files.pythonhosted.org/packages/29/c1/24814557f1d22c56d50280771a17307e6bf87b70727d975fd6b2ce6b014a/requests-2.25.1-py2.py3-none-any.whl\n  homepage: https://requests.readthedocs.io\n  git_url: https://github.com/psf/requests\n  updated_at: "2021-02-22T17:32:25.323561"\n- domain: pypi\n  name: idna\n  version: "2.10"\n  licenses:\n    - spdx_id: BSD-3-Clause\n      basis: API_LATEST\n      source_url: https://pypi.org/pypi/idna/json\n    - spdx_id: BSD-3-Clause\n      basis: GITHUB_LICENSES_API\n      source_url: https://api.github.com/repos/kjd/idna/license\n  download_url: https://files.pythonhosted.org/packages/a2/38/928ddce2273eaa564f6f50de919327bf3a00f091b5baba8dfa9460f3a8a8/idna-2.10-py2.py3-none-any.whl\n  homepage: https://github.com/kjd/idna\n  git_url: https://github.com/kjd/idna\n  updated_at: "2021-02-22T17:32:24.035106"\n```\n\n**Ruby libraries**\n\n```console\n$ bundle list > bundle-list.txt\n$ lilili search --yaml bundle-list.txt\n```\n\nThe output `result.yml` is in the same format as above.\n\n**Node.js libraries**\n\n```console\n$ yarn list > yarn-list.txt\n$ lilili search --yaml yarn-list.txt\n```\n\nThe output `result.yml` is in the same format as above.\n\n## Why LiLiLi?\n\n* LiLiLi uses [the SPDX license list](https://spdx.org/licenses/), which is also used by [GitHub Licenses API](https://docs.github.com/en/rest/reference/licenses), so the license notation can be reused.\n* If LiLiLi cannot determine the license for a particular version of the library, it will search for the latest version of the license or a license registered in the GitHub repository.\n* LiLiLi will reveal the URL of the API on which the licensing decision is based, so you can double-check it yourself.\n',
    'author': 'poyo46',
    'author_email': 'poyo4rock@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/poyo46/lilili',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
