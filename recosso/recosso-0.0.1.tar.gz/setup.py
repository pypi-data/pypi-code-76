from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='recosso',
  version='0.0.1',
  description='Official package of recosso',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Himanshu Sahrawat',
  author_email='hsdsahrawat@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='recosso', 
  packages=find_packages(),
  install_requires=['pandas','numpy','plotly'] 
)