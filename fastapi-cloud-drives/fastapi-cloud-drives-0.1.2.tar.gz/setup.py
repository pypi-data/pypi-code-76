# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_cloud_drives']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.63.0,<0.64.0',
 'google-api-python-client>=1.12.8,<2.0.0',
 'google-auth-oauthlib>=0.4.2,<0.5.0',
 'oauth2client>=4.1.3,<5.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'uvicorn>=0.13.3,<0.14.0']

setup_kwargs = {
    'name': 'fastapi-cloud-drives',
    'version': '0.1.2',
    'description': 'Module for FastAPI to work with cloud drives',
    'long_description': '<h3 align="center">FastAPI Cloud Drives</h3>\n\n<div align="center">\n\n[![Status](https://img.shields.io/badge/status-active-success.svg)]()\n[![GitHub Issues](https://img.shields.io/github/issues/kylelobo/The-Documentation-Compendium.svg)](https://github.com/MadeByMads/fastapi-cloud-drives/issues)\n[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/kylelobo/The-Documentation-Compendium.svg)](https://github.com/MadeByMads/fastapi-cloud-drives/pulls)\n[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)\n\n</div>\n\n\n## 🧐 About <a name = "about"></a>\n\nThe FastAPI Cloud Drives module supports Google Drive, OneDrive, Dropbox cloud storage providers. You can easily search, upload, download files from this cloud providers. \n\n\n## 🏁 Getting Started <a name = "getting_started"></a>\n\n### Installing\n\n```bash\npip install fastapi-cloud-drives\n```\n\n## 🎈 Usage <a name="usage"></a>\n\n\nSee also the list of [contributors](https://github.com/MadeByMads/fastapi-cloud-drives/graphs/contributors) who participated in this project.\n\n\n## Contributing\nWe are open to  new ideas, additions. If you have any we would be happy to recieve and diccuss.',
    'author': 'Hasan Aliyev',
    'author_email': 'hasan.aliyev.555@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MadeByMads/fastapi-cloud-drives',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
