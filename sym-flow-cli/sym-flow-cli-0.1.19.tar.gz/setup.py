# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flow',
 'flow.cli',
 'flow.cli.commands',
 'flow.cli.commands.debug',
 'flow.cli.commands.integrations',
 'flow.cli.commands.integrations.slack',
 'flow.cli.helpers',
 'flow.cli.helpers.login',
 'flow.cli.models',
 'flow.cli.tests',
 'flow.cli.tests.commands',
 'flow.cli.tests.commands.debug',
 'flow.cli.tests.commands.integrations',
 'flow.cli.tests.helpers',
 'flow.cli.tests.helpers.iam_policies',
 'flow.cli.tests.helpers.login']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'analytics-python>=1.2.9,<2.0.0',
 'boto3>=1.16.20,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'immutables>=0.14,<0.15',
 'pkce>=1.0,<2.0',
 'policy-sentry==0.9.0',
 'policyuniverse>=1.3.2,<2.0.0',
 'portalocker>=2.0.0,<3.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'sentry-sdk>=0.19.3,<0.20.0',
 'sym-cli==0.1.22',
 'tabulate>=0.8.7,<0.9.0',
 'validators>=0.18.1,<0.19.0']

entry_points = \
{'console_scripts': ['symflow = sym.flow.cli.symflow:symflow']}

setup_kwargs = {
    'name': 'sym-flow-cli',
    'version': '0.1.19',
    'description': "Sym's Official CLI for Implementers",
    'long_description': '# sym-flow-cli\n\nThis is the official CLI for [Sym](https://symops.com/) Implementers. Check out the docs [here](https://docs.symops.com/docs/install-sym-flow).\n',
    'author': 'SymOps, Inc.',
    'author_email': 'pypi@symops.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://symops.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
