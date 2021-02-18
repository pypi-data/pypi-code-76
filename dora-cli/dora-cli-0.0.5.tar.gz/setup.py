# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dora_cli']

package_data = \
{'': ['*']}

install_requires = \
['clint>=0.5.1,<0.6.0',
 'docker>=4.4.2,<5.0.0',
 'docopt>=0.6.2,<0.7.0',
 'esdk-obs-python>=3.20.11,<4.0.0',
 'huaweicloud-sdk-python>=1.0.28,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'tabulate>=0.8.7,<0.9.0']

setup_kwargs = {
    'name': 'dora-cli',
    'version': '0.0.5',
    'description': 'Dora Command Line Interface',
    'long_description': '# Dora CLI\n\nCommand Line Interface to manager an Dora sandbox.\n\n```sh\npython -m dora_cli\n```\n\n## Usage \n\nThe following options are available in this version:\n\n## `configure`\n\nUse to setup your environment with all the credentials and configurations needed to access the Cloud Provider services.\n\nAll the configurations will be saved on `~/.config/dora-cli/config.json`\n\n> Use `--help` option to more details\n\n## `start`\n\nIf successful you will be prompted with the **token** generated to access you Jupyter Lab environment followed by **name** and **status** of the *container*.\n\n```txt\nTOKEN:d337b5ee0b72c6687b9a9e8f8f9a2f5972559454e90c6e10\nhappy_lovelace:created\n```\n\nAccess the application by `http://<public-ip>:8888/lab?token=d337b5ee0b72c6687b9a9e8f8f9a2f5972559454e90c6e10`\n\n> Use `--help` option to more details\n\n\n## Requirements\n\nThe following packages are needed on the Operating System to run this application:\n\n- python3.7\n- pip \n- docker \n- nfs-common\n\n```sh\n# setup on Ubuntu linux\nsudo apt install -y python3 python3-pip python3-setuptools docker.io nfs-common\n```\n\n> [Mounting an NFS File System to ECSs (Linux)](https://support.huaweicloud.com/intl/en-us/qs-sfs/en-us_topic_0034428728.html)\n',
    'author': 'didone',
    'author_email': 'didone@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/doraproject/cli.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
