# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['authcaptureproxy', 'authcaptureproxy.examples']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.3,<4.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'importlib-metadata>=3.4.0,<4.0.0',
 'multidict>=5.1.0,<6.0.0',
 'typer>=0.3,<1.0',
 'yarl>=1.6.3,<2.0.0']

entry_points = \
{'console_scripts': ['auth_capture_proxy = authcaptureproxy.cli:cli']}

setup_kwargs = {
    'name': 'authcaptureproxy',
    'version': '0.4.2',
    'description': 'A Python project to create a proxy to capture authentication information from a webpage. This is useful to capture oauth login details without access to a third-party oauth.',
    'long_description': '# Auth_capture_proxy\n\n[![Version status](https://img.shields.io/pypi/status/authcaptureproxy)](https://pypi.org/project/authcaptureproxy)\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n[![Python version compatibility](https://img.shields.io/pypi/pyversions/authcaptureproxy)](https://pypi.org/project/authcaptureproxy)\n[![Version on Github](https://img.shields.io/github/v/release/alandtse/auth_capture_proxy?include_prereleases&label=GitHub)](https://github.com/alandtse/auth_capture_proxy/releases)\n[![Version on PyPi](https://img.shields.io/pypi/v/authcaptureproxy)](https://pypi.org/project/authcaptureproxy)\n![PyPI - Downloads](https://img.shields.io/pypi/dd/authcaptureproxy)\n![PyPI - Downloads](https://img.shields.io/pypi/dw/authcaptureproxy)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/authcaptureproxy)\n[![Documentation Status](https://readthedocs.org/projects/auth-capture-proxy/badge/?version=latest)](https://auth-capture-proxy.readthedocs.io/en/latest/?badge=latest)\n[![Build (Github Actions)](https://img.shields.io/github/workflow/status/alandtse/auth_capture_proxy/Build%20&%20test?label=Build%20&%20test)](https://github.com/alandtse/auth_capture_proxy/actions)\n[![Test coverage (coveralls)](https://coveralls.io/repos/github/alandtse/auth_capture_proxy/badge.svg?branch=main&service=github)](https://coveralls.io/github/alandtse/auth_capture_proxy?branch=main)\n\nA Python project to create a proxy to capture authentication information from a webpage. This is useful to capture oauth login details without access to a third-party oauth.\n\n## Install\n\n```bash\npip install authcaptureproxy\n```\n\n## Using\n\nTo see basic usage look at the [proxy-example](authcaptureproxy/cli.py) that logs into Amazon.com and will print out the detected email and password.\n\n```bash\npython authcaptureproxy/cli.py proxy-example\n```\n\n[See the docs 📚](https://auth-capture-proxy.readthedocs.io/en/latest/) for more info.\n\n## License\n\nLicensed under the terms of the [Apache License 2.0](https://spdx.org/licenses/Apache-2.0.html).\n\n## Contributing\n\n[New issues](https://github.com/alandtse/auth_capture_proxy/issues) and pull requests are welcome.\nPlease refer to the [contributing guide](https://github.com/alandtse/auth_capture_proxy/blob/main/CONTRIBUTING.md)\nand [security policy](https://github.com/alandtse/auth_capture_proxy/blob/main/SECURITY.md).\n\nGenerated with [Tyrannosaurus](https://github.com/dmyersturnbull/tyrannosaurus).\n',
    'author': 'Alan D. Tse',
    'author_email': None,
    'maintainer': 'Alan D. Tse',
    'maintainer_email': None,
    'url': 'https://github.com/alandtse/auth_capture_proxy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
