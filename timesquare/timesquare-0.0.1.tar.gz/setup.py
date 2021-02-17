from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='timesquare',
  version='0.0.1',
  description='Solve Quadratic Equations',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Ilay Furst',
  author_email='furstilay11@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='quadratic',
  packages=find_packages(),
  install_requires=[''] 
)
