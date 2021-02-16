"""
Your licence goes here
"""
 
from setuptools import setup, find_packages
 
# See note below for more information about classifiers
classifiers = [
  'Development Status :: 3 - Alpha',
  'Intended Audience :: Science/Research',
  "Operating System :: OS Independent",
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='PyFuzzySet',
  version='0.0.3',
  description='Includes Fuzzy Set Algorithms, Intuitionistic Fuzzy Set Algorithms and Fuzzy Cluster Validity Indexes',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://github.com/ibrahimayaz/PyFuzzySet',  # the URL of your package's home page e.g. github link
  author='İbrahim AYAZ, Fatih KUTLU',
  author_email='ayazibrahim13@gmail.com',
  license='MIT', # note the American spelling
  classifiers=classifiers,
  keywords='', # used when people are searching for a module, keywords separated with a space
  packages=find_packages(),
  install_requires=[''] # a list of other Python modules which this module depends on.  For example RPi.GPIO
)