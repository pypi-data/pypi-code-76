# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqredirect']

package_data = \
{'': ['*']}

install_requires = \
['pyroute2>=0.4']

extras_require = \
{':python_version >= "2.7" and python_version < "3.0"': ['py2-ipaddress>=3.4.2,<4.0.0']}

entry_points = \
{'console_scripts': ['sqredirect = sqredirect.redirect:sqredirect']}

setup_kwargs = {
    'name': 'sqredirect',
    'version': '1.2.0',
    'description': '',
    'long_description': '# sqredirect\n\nRedirection and filtering Source Engine game traffic in a bundle with [sqproxy](https://github.com/sqproxy/sqproxy)\n\n\n## How it Works?\n\n**sqredirect** attach eBPF filter(s) to network interface and manipulate with traffic targeting to game ports\n\neBPF is more efficient way to check/accept/drop packets in Linux\n\n[More in Wikipedia](https://en.wikipedia.org/wiki/Berkeley_Packet_Filter)\n\n\n## Requirements\n\n* Linux\n* Kernel version >= 4.4, check your by command: uname -r\n* python2 or python3\n\n\n## Installation\n\nTODO: Split into Ubuntu/Debian/Others like in bcc-tools README\n\n### Step 1: Install bcc-tools\n\n* bcc-tools >= 0.10.0 (depends on Kernel version, see https://github.com/iovisor/bcc/releases)\n    - [Install instruction (non-Debian 10)](https://github.com/iovisor/bcc/blob/master/INSTALL.md)\n    - [Install instruction (Debian 10)](https://github.com/iovisor/bcc/issues/3081#issuecomment-766422307)\n    - You can check the current version via ``python -c \'import bcc; print(bcc.__version__);\'``\n\n### Step 2: Install sqredirect\n\n    python -m pip install sqredirect\n\nhttps://pypi.org/project/sqredirect/\n\n## Usage\n\n### Automatically\n\nOnly by [SQProxy](https://github.com/sqproxy/sqproxy)\n\n### Non-root running\n\nbcc-tools can\'t be used w/o root, see https://github.com/iovisor/bcc/issues/1166\n\nBut you can use this snippet to restrict usage only to specified user/group:\n\n**TL;DR:** move `python redirect.py $@` to command and add permissions in `/etc/sudoers`\n\n---\n\n1. Copy content of this folder to `/usr/src/sqredirect`\n\n1. Create file in `/usr/local/bin/sqredirect` with content: \n\n    ```bash\n    #!/bin/bash\n    \n    cd /usr/src/sqredirect\n    exec python2 /usr/src/sqredirect/redirect.py $@\n    ```\n\n1. `chmod +x /usr/local/bin/sqredirect`\n\n1. Create group network and add user to group\n\n    ```bash\n    addgroup network\n    usermod -aG network <user-which-should-it-run>\n    ```\n\n1. Allow run `sqredirect` command w/o root privileges\n\n    ```bash\n    echo "%network ALL=(root) NOPASSWD: /usr/local/bin/sqredirect" > /etc/sudoers.d/network\n    ```\n\nMore about sudoers: https://www.digitalocean.com/community/tutorials/how-to-edit-the-sudoers-file\n\n\n## Troubleshooting\n\n**Problem:** I can\'t reach my server through network\n\n**Solution:** Rollback any changes at network level, run in console (if you have access): \n\n    tc qdisc del dev eth0 root\n\nreplace `eth0` with your interface name\n',
    'author': 'spumer',
    'author_email': 'spumer-tm@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=2.7,<4',
}


setup(**setup_kwargs)
