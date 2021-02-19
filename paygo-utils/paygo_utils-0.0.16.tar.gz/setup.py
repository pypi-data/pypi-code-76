from setuptools import setup, find_packages

classifiers = [
   'Development Status :: 5 - Production/Stable',
   'Intended Audience :: Developers',
   'Operating System :: Microsoft :: Windows :: Windows 10',
   'License :: OSI Approved :: MIT License',
   'Programming Language :: Python :: 3'
]

setup(
   name='paygo_utils',
   version='0.0.16',
   description='This is a utilities library that contains the base files needed by every microservice',
   long_description=open('README.txt').read() +'\n\n'+ open('CHANGELOG.txt').read(),
   url='',
   author='Umar Kayondo',
   author_email='umabravo70@gmail.com',
   license='MIT',
   classifiers=classifiers,
   keywords='paygo utils',
   packages=['paygo_utils'],
   install_requires=['']
)