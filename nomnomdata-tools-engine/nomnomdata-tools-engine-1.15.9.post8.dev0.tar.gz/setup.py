# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nomnomdata',
 'nomnomdata.tools.engine',
 'nomnomdata.tools.engine.template',
 'nomnomdata.tools.engine.template.pkg',
 'nomnomdata.tools.engine.template.pkg.tests']

package_data = \
{'': ['*']}

install_requires = \
['aiobotocore[boto3]>=1.1.1,<2.0.0',
 'cerberus>=1.3.2,<2.0.0',
 'click-pathlib>=2020.3.13,<2021.0.0',
 'docker-compose>=1.26.2,<2.0.0',
 'docker[ssh]>=4.3.1,<5.0.0',
 'dunamai>=1.3.0,<2.0.0',
 'fsspec>=0.8.0,<0.9.0',
 'jinja2>=2.11.2,<3.0.0',
 'nomnomdata-auth>=2.3.4,<3.0.0',
 'nomnomdata-cli>=0.1.8,<0.2.0',
 'pyyaml>=5.3.1,<6.0.0',
 'requests>=2.23.0,<3.0.0',
 's3fs>=0.5.0,<0.6.0']

entry_points = \
{'nomnomdata.cli_plugins': ['engine-tools = nomnomdata.tools.engine.cli:cli']}

setup_kwargs = {
    'name': 'nomnomdata-tools-engine',
    'version': '1.15.9.post8.dev0',
    'description': 'Package containing tooling for developing nominode engines',
    'long_description': '# Installation\n\n`pip install nomnomdata-tools-engine nomnomdata-engine`\n\n# Creating a new app\n\nInstructions for how to create, build and deploy a new app available here:\n\n<https://support.nomnomdata.com/portal/en/kb/articles/creating-your-first-nnd-app>\n\nAdditional toolkit information available here:\n\n<http://developer.nomnomdata.com/>\n',
    'author': 'Nom Nom Data Inc',
    'author_email': 'info@nomnomdata.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/nomnomdata/tools/nomnomdata-tools-engine',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.4,<4.0.0',
}


setup(**setup_kwargs)
