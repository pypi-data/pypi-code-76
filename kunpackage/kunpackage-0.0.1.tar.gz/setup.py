from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='kunpackage',
  version='0.0.1',
  description='A very basic action package',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',
  author='Kun Zhang',
  author_email='kuzhang@paloaltonetworks.com',
  license='MIT',
  classifiers=classifiers,
  keywords='test',
  packages=find_packages(),
  install_requires=['']
)