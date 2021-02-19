from setuptools import setup, find_packages
setup(
  name = 'snmp_requests',
  version='0.0.7',
  description = 'SNMP library developed for Network Management classes at University of Zaragoza. This library has been developed with teaching purposes and is based on pysnmp library.',
  author = 'Jorge Sancho',
  author_email = 'jslarraz@gmail.com',
  url = 'https://github.com/jslarraz/snmp_requests', # use the URL to the github repo

  packages=find_packages(),
  install_requires=[
    'pysnmp',
  ],

  #download_url = 'https://github.com/jslarraz/fhirtools/tarball/0.1',
  keywords = ['snmp', 'development'],
  classifiers = [],
)
