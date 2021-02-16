# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dsnap']

package_data = \
{'': ['*'], 'dsnap': ['files/*']}

install_requires = \
['boto3>=1.16.0,<2.0.0']

extras_require = \
{'cli': ['typer>=0.3.2,<0.4.0']}

entry_points = \
{'console_scripts': ['dsnap = dsnap.main:app']}

setup_kwargs = {
    'name': 'dsnap',
    'version': '0.1.9',
    'description': "Utility for downloading EBS snapshots using the EBS Direct API's",
    'long_description': '![Python package](https://github.com/RhinoSecurityLabs/dsnap/workflows/Python%20package/badge.svg?branch=main)\n\n# DSnap\n\nUtility for downloading EBS snapshots using the EBS Direct API\'s.\n\n## Install\n\n### PyPi\n\n```shell\n=======\n```\n% pip install -U pip\n% pip install \'dsnap[cli]\'\n```\n\n## Command Reference\n\n```shell\n% dsnap --help\nUsage: dsnap [OPTIONS] COMMAND [ARGS]...\n\n  A utility for managing snapshots via the EBS Direct API.\n\nOptions:\n  --region REGION                 Sets the AWS region.  [default: us-east-1]\n  --profile PROFILE               Shared credential profile to use.\n  --install-completion [bash|zsh|fish|powershell|pwsh]\n                                  Install completion for the specified shell.\n  --show-completion [bash|zsh|fish|powershell|pwsh]\n                                  Show completion for the specified shell, to\n                                  copy it or customize the installation.\n\n  --help                          Show this message and exit.\n\nCommands:\n  create  Create a snapshot for the given instances default device volume.\n  delete  Delete a given snapshot.\n  get     Download a snapshot for a given instance or snapshot ID.\n  init    Write out a Vagrantfile template to explore downloaded snapshots.\n  list    List snapshots in AWS.\n```\n\n## Examples\n\n### Recording\n\n[![asciicast](https://asciinema.org/a/391559.svg)](https://asciinema.org/a/391559)\n\n### Listing Snapshots\n```shell\n% dsnap list\n           Id          |   Owner ID   |   State\nsnap-0dbb0347f47e38b96   922105094392   completed\n```\n\n### Downloading a Snapshot\n```shell\n% dsnap get snap-0dbb0347f47e38b96\nOutput Path: /cwd/snap-0dbb0347f47e38b96.img\n```\n\nIf you don\'t specify a snapshot  you\'ll get a prompt to ask which one you want to download:\n```shell\n% dsnap chris get\n0) i-01f0841393cd39f06 (ip-172-31-27-0.ec2.internal, vpc-04a91864355539a41, subnet-0e56cd55282fa9158)\nSelect Instance: 0\n0) vol-0a1aab48b0bc3039d (/dev/sdb)\n1) vol-0c616d718ab00e70c (/dev/xvda)\nSelect Volume: 0\nNo snapshots found, create one? [y/N]: y\nCreating snapshot for Instance(s): i-01f0841393cd39f06 /dev/sdb, Volume: vol-0a1aab48b0bc3039d\nWaiting for snapshot to complete.\nOutput Path: /cwd/snap-0dbb0347f47e38b96.img\nCleaning up snapshot: snap-0543a8681adce0086\n```\n\n### Mounting in Vagrant\nThis requires virtualbox to be installed. dsnap init will write a Vagrantfile to the current directory that can be used to mount a specific downloaded snapshot. Conversion to a VDI disk is handled in the Vagrantfile, it will look for the disk file specified in the IMAGE environment variable, convert it to a VDI using `VBoxManage convertdd`. The resulting VDI is destroyed when the Vagrant box is, however the original raw .img file will remain and can be reused as needed.\n\n```shell\n% dsnap init\n% IMAGE=snap-0543a8681adce0086.img vagrant up\n% vagrant ssh\n```\n\n### Mounting With Docker\n\nThis uses libguestfs to work directly with the downloaded img file.\n\n#### Build Docker Container\n```shell\n% git clone https://github.com/RhinoSecurityLabs/dsnap.git\n% cd dsnap\n% make docker/build\n```\n\n#### Run Guestfish Shell\n\n```shell\n% IMAGE=snap-0dbb0347f47e38b96.img make docker/run\n```\n\nThis will take a second to start up. After it drops you into the shell you should be able to run commands like ls, cd, cat. However worth noting they don\'t always behave exactly like they do in a normal shell.\n\nThe output will give you the basics of how to use the guestfish shell. For a full list of command you can run `help --list`.\n\nBelow is an example of starting the shell and printing the contents of /etc/os-release.\n\n```shell\n% IMAGE=snap-0dbb0347f47e38b96.img make docker/run\ndocker run -it -v "/cwd/dsnap/snap-0dbb0347f47e38b96.img:/disks/snap-0dbb0347f47e38b96.img" -w /disks mount --ro -a "snap-0dbb0347f47e38b96.img" -m /dev/sda1:/\n\nWelcome to guestfish, the guest filesystem shell for\nediting virtual machine filesystems and disk images.\n\nType: ‘help’ for help on commands\n      ‘man’ to read the manual\n      ‘quit’ to quit the shell\n\n><fs> cat /etc/os-release\nNAME="Amazon Linux"\nVERSION="2"\nID="amzn"\nID_LIKE="centos rhel fedora"\nVERSION_ID="2"\nPRETTY_NAME="Amazon Linux 2"\nANSI_COLOR="0;33"\nCPE_NAME="cpe:2.3:o:amazon:amazon_linux:2"\nHOME_URL="https://amazonlinux.com/"\n```\n\n\n## Development\n\nFor CLI development make sure you include the `cli` extra shown below. You\'ll also want to invoke the package by using python\'s `-m` (shown below) for testing local changes, the dnsap binary installed to the environment will only update when you run pip install.\n\n### Setup\n```shell\n% git clone https://github.com/RhinoSecurityLabs/dsnap.git\n% cd dsnap\n% python3 -m venv venv\n% . venv/bin/activate\n% python -m pip install \'.[cli]\'\n```\n\n### Running With Local Changes\n```shell\n% python -m dsnap --help\n```\n\n### Linting and Type Checking\n```shell\n% make lint\n```\n\n### Testing\n```shell\n% make test\n```\n\n',
    'author': 'Ryan Gerstenkorn',
    'author_email': 'ryan.gerstenkorn@rhinosecuritylabs.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
