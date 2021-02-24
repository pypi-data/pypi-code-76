from setuptools import setup
import ast
import sys

setup_requires = ['setuptools >= 30.4.7']
if {'pytest', 'test', 'ptr'}.intersection(sys.argv):
    setup_requires.append('pytest-runner')

# Get docstring and version without importing module
#with open('coff/__init__.py') as f:
#    mod = ast.parse(f.read())

__doc__ = ""
__version__ = ""
#__doc__ = ast.get_docstring(mod)
#__version__ = mod.body[-1].value.s

setup(description=__doc__,
      long_description=__doc__,
      version= '0.4.7', 
      setup_requires=setup_requires)
