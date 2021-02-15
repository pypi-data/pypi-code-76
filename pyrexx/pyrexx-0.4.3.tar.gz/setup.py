import setuptools

setuptools.setup(
    name='pyrexx',
    version='0.4.3',
    author='Guilherme Cartier',
    description='Python library that enables parsing and analysis of REXX source code',
    packages=['pyrexx',
              'pyrexx.rexx',
              'pyrexx.rexx.statements',
              'pyrexx.utilities',
              'pyrexx.exceptions'],
    python_requires='>=3.6'
)
