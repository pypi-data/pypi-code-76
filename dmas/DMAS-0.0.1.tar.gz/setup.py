  
from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='dmas',
  version='0.0.1',
  description='two number are taking enter from user and the applying the DMAS rule',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Raza Rizwan',
  author_email='rrizwan1998@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='dmas', 
  packages=find_packages(),
  install_requires=[''] 
)