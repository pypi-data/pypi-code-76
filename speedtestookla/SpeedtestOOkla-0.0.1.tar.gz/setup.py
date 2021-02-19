from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='SpeedtestOOkla',
  version='0.0.1',
  description='Okla Speed test automation',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Amrit Lal Gaur',
  author_email='amrit.gaur549@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='speedtestautomation',
  packages=find_packages(),
  install_requires=[''] 
)
