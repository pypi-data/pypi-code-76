# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sysaudit']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sysaudit',
    'version': '0.3.0',
    'description': 'Backport module for sys.audit and sys.addaudithook from Python 3.8',
    'long_description': 'sysaudit\n========\n.. image:: https://readthedocs.org/projects/sysaudit/badge/?version=latest\n  :target: https://sysaudit.readthedocs.io/en/latest/?badge=latest\n  :alt: Documentation Status\n\n.. image:: https://github.com/brettlangdon/sysaudit/workflows/Build/badge.svg?branch=main&event=push\n  :target: https://github.com/brettlangdon/sysaudit/actions?query=branch%3Amain+workflow%3ABuild+event%3Apush\n  :alt: Build status\n\nBackport module of `sys.audit <https://docs.python.org/3.8/library/sys.html#sys.audit>`_\nand `sys.addaudithook <https://docs.python.org/3.8/library/sys.html#sys.addaudithook>`_\nfrom Python 3.8.\n\n**Note:** This module does *not* backport any of the built-in\n`audit events <https://docs.python.org/3.8/library/audit_events.html#audit-events>`_.\n\n\nInstallation\n------------\n\n.. code-block:: bash\n\n    pip install sysaudit\n\nQuick Usage\n-----------\n\n`sysaudit` can be used as a drop-in replacement for `sys.audit` and `sys.addaudithook`.\n\n.. code-block:: python\n\n  import sysaudit\n\n  def hook(event, args):\n      print("Event:", event, args)\n\n  sysaudit.addaudithook(hook)\n\n  sysaudit.audit("event_name", 1, 2, dict(key="value"))\n  # Event: event_name (1, 2, {\'key\': \'value\'})\n',
    'author': 'brettlangdon',
    'author_email': 'me@brett.is',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://sysaudit.readthedocs.io/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
