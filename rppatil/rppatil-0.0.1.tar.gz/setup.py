from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: POSIX :: Linux',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='rppatil',
  version='0.0.1',
  description='reads and writes jsons',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Rahul P Patil',
  author_email='rahulpp891994@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='read and write jsons', 
  packages=find_packages(),
  install_requires=[''] 
)