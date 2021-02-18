from setuptools import setup
 
setup(
  name='reportlabtyphon',
  version='1.0.0',
  description='A print test for PyPI',
  author='rrd',
  author_email='rrd@rrd.com',
  url='https://www.python.org/',
  license='MIT',
  keywords='ga nn',
  project_urls={
   'Documentation': 'https://packaging.python.org/tutorials/distributing-packages/',
   'Funding': 'https://donate.pypi.org',
   'Source': 'https://github.com/pypa/sampleproject/',
   'Tracker': 'https://github.com/pypa/sampleproject/issues',
  },
  packages=['reportlabtyphon'],
  install_requires=['numpy>=1.14', 'tensorflow>=1.7'],
  python_requires='>=3'
  )