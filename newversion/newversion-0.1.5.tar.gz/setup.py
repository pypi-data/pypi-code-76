# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['newversion']

package_data = \
{'': ['*']}

install_requires = \
['packaging>=20.0,<21.0', 'typing-extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'newversion',
    'version': '0.1.5',
    'description': 'PEP 440 version manager',
    'long_description': '# NewVersion - Your version manager\n\n[![PyPI - newversion](https://img.shields.io/pypi/v/newversion.svg?color=blue&label=newversion)](https://pypi.org/project/newversion)\n[![Docs](https://img.shields.io/readthedocs/newversion.svg?color=blue&label=Builder%20docs)](https://newversion.readthedocs.io/)\n\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/newversion.svg?color=blue)](https://pypi.org/project/newversion)\n[![Coverage](https://img.shields.io/codecov/c/github/vemel/newversion)](https://codecov.io/gh/vemel/newversion)\n\n- [NewVersion - Your version manager](#newversion---your-version-manager)\n  - [Features](#features)\n  - [Installation](#installation)\n  - [Usage](#usage)\n    - [CLI](#cli)\n    - [Python library](#python-library)\n  - [Versioning](#versioning)\n  - [Latest changes](#latest-changes)\n\n## Features\n\n- Follows [PEP 440](https://www.python.org/dev/peps/pep-0440/)\n- Fully compatible with [packaging.Version](https://packaging.pypa.io/en/latest/version.html)\n- Brings version bumping from [semver](https://pypi.org/project/semver/)\n- Comes with a helpful CLI tool `newversion`\n- Shines in CI\n\n## Installation\n\n```bash\npython -m pip install newversion\n```\n\n## Usage\n\n### CLI\n\n```bash\nnewversion            # 0.0.0\nnewversion bump major # 1.0.0\n\npython setup.py --version  # 1.2.3\npython setup.py --version | newversion bump  # 1.2.4\npython setup.py --version | newversion get minor  # 2\n\necho "1.2.3rc1" | newversion bump micro   # 1.2.3\necho "1.2.3rc1" | newversion bump minor   # 1.3.0\necho "1.2.3rc1" | newversion bump major   # 2.0.0\necho "1.2.3rc1" | newversion bump pre     # 1.2.3rc2\necho "1.2.3rc1" | newversion bump rc      # 1.2.3rc2\necho "1.2.3rc1" | newversion bump alpha   # 1.2.4a1\n\necho "1.2.3rc1" | newversion set micro 5  # 1.2.5rc1\necho "1.2.3rc1" | newversion set minor 5  # 1.5.3rc1\necho "1.2.3rc1" | newversion set major 5  # 5.2.3rc1\necho "1.2.3rc1" | newversion set pre 5    # 1.2.3rc5\necho "1.2.3rc1" | newversion set rc 5     # 1.2.3rc5\necho "1.2.3rc1" | newversion set alpha 5  # 1.2.3a5\n\necho "1.2.3rc1" | newversion get micro    # 1\necho "1.2.3rc1" | newversion get minor    # 2\necho "1.2.3rc1" | newversion get major    # 3\necho "1.2.3rc1" | newversion get pre      # rc1\necho "1.2.3rc1" | newversion get rc       # 1\necho "1.2.3rc1" | newversion get alpha    # 0\n\necho "1.2.3rc1" | newversion stable # 1.2.3\n\necho "1.2.3rc1" | newversion is_stable       # error!\necho "1.2.3" | newversion is_stable          # 1.2.3\necho "1.2.3" | newversion is_stable && echo "Stable!" # Stable!\n\necho "1.2.3rc1" | newversion gt "1.2.3"   # error!\necho "1.2.3rc1" | newversion lte "1.2.3"  # "1.2.3rc1"\n```\n\n### Python library\n\n```python\nfrom newversion import Version\n\nversion = Version("1.2.3")\nnext_version = version.bump_minor() # Version("1.3.0")\n\n# bump version same way as SemVer\nversion.dumps() # "1.2.3"\nversion.bump_micro().dumps() # "1.2.4"\nversion.bump_minor().dumps() # "1.3.0"\nversion.bump_major().dumps() # "2.0.0"\n\n# create and bump pre-releases\nversion.bump_prerelease().dumps() # "1.2.4rc1"\nversion.bump_prerelease(bump_release="minor").dumps() # "1.3.0rc1"\nversion.bump_prerelease("alpha").dumps() # "1.2.4a1"\nVersion("1.2.3b4").bump_prerelease().dumps() # "1.2.3b5"\nversion.bump_micro().replace(dev=1234).dumps() # "1.2.4.dev1234"\n\n# and post-releases\nversion.bump_postrelease().dumps() # "1.2.3.post1"\nVersion("1.2.3.post3").bump_postrelease(2).dumps() # "1.2.3.post5"\n\n# easily check if this is a pre- or dev release or a stable version\nVersion("1.2.3").is_stable # True\nVersion("1.2.3a6").is_stable # False\nVersion("1.2.3.post3").is_stable # True\nVersion("1.2.3.post3").get_stable().dumps() # "1.2.3"\n```\n\n## Versioning\n\n`newversion` version follows [PEP 440](https://www.python.org/dev/peps/pep-0440/).\n\n## Latest changes\n\nFull changelog can be found in [Releases](https://github.com/vemel/newversion/releases).\n',
    'author': 'Vlad Emelianov',
    'author_email': 'vlad.emelianov.nz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vemel/newversion',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.10,<4.0.0',
}


setup(**setup_kwargs)
