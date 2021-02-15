#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['stepwise_mol_bio', 'stepwise_mol_bio.gels']

package_data = \
{'': ['*'], 'stepwise_mol_bio': ['layouts/*']}

install_requires = \
['appdirs',
 'autoprop',
 'configurator',
 'docopt',
 'inform>=1.21',
 'numpy',
 'pytest',
 'requests',
 'stepwise',
 'voluptuous']

extras_require = \
{'docs': ['sphinx', 'sphinx_rtd_theme', 'autoclasstoc'],
 'tests': ['pytest', 'pytest-cov', 'coveralls', 'toml']}

entry_points = \
{'po4.syntheses': ['PCR = stepwise_mol_bio.pcr:Po4Synthesis'],
 'stepwise.protocols': ['molbio = stepwise_mol_bio:Plugin']}

setup(name='stepwise_mol_bio',
      version='1.9.1',
      description='Protocols relating to molecular biology, e.g. PCR.',
      author='Kale Kundert',
      author_email='kale@thekunderts.net',
      url='https://github.com/kalekundert/stepwise_mol_bio',
      packages=packages,
      package_data=package_data,
      install_requires=install_requires,
      extras_require=extras_require,
      entry_points=entry_points,
      python_requires='~=3.8',
     )
