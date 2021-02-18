# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['canonicalwebteam', 'canonicalwebteam.candid']

package_data = \
{'': ['*']}

install_requires = \
['pymacaroons==0.13.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'canonicalwebteam.candid',
    'version': '0.9.0',
    'description': '',
    'long_description': '# Canonical Candid - Python package\n\n[![Test live APIs](https://github.com/canonical-web-and-design/canonicalwebteam.store-api/workflows/Test%20live%20APIs/badge.svg)](https://github.com/canonical-web-and-design/canonicalwebteam.store-api/actions?query=workflow%3ATest%20live%20APIs)\n[![Tests](https://github.com/canonical-web-and-design/canonicalwebteam.store-api/workflows/Tests/badge.svg)](https://github.com/canonical-web-and-design/canonicalwebteam.store-api/actions?query=workflow%3A)\n[![Publish](https://github.com/canonical-web-and-design/canonicalwebteam.store-api/workflows/Publish/badge.svg)](https://github.com/canonical-web-and-design/canonicalwebteam.store-api/actions?query=workflow%3APublish)\n[![Code coverage](https://codecov.io/gh/canonical-web-and-design/canonicalwebteam.store-api/branch/master/graph/badge.svg)](https://codecov.io/gh/canonical-web-and-design/canonicalwebteam.store-api)\n\ncanonicalwebteam.candid provides authentication with Candid, a macaroon-based\nauthentication service.\n\n\nSee: https://github.com/canonical/candid\n\n\nThis client only support the browser-redirect login protocol that\nprovides a mechanism for a user to authenticate with candid, and\nsubsequently discharge macaroons, by redirecting a web browser via\nthe candid login pages.\n\n## How to install\n\nTo install this extension as a requirement in your project, you can use PIP:\n\n```bash\npip install canonicalwebteam.candid\n```\n\nSee also the documentation for [pip install](https://pip.pypa.io/en/stable/reference/pip_install/).\n\n## Development\n\nThe package leverages [poetry](https://poetry.eustace.io/) for dependency management.\n',
    'author': 'Canonical Web Team',
    'author_email': 'webteam@canonical.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
