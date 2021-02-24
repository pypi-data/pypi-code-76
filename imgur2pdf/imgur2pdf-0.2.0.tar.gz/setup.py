# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['imgur2pdf', 'upload2remarkable']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.0.1,<9.0.0',
 'click>=7.1.2,<8.0.0',
 'imgurpython>=1.1.7,<2.0.0',
 'requests>=2.24.0,<3.0.0',
 'rmapy>=0.2.3,<0.3.0']

entry_points = \
{'console_scripts': ['imgur2pdf = imgur2pdf:main',
                     'upload2remarkable = upload2remarkable:main']}

setup_kwargs = {
    'name': 'imgur2pdf',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'mrfyda',
    'author_email': 'mrfyda@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
