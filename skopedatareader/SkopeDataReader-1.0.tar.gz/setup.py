from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='SkopeDataReader',
      version='1.0',
      description = 'Python reader to load data acquired with skope-fm or skope-fx',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Yolanda Duerst',
      author_email='yolanda.duerst@skope.ch',
      packages=['SkopeDataReader'],
      install_requires=[
          'numpy', 'scipy',
      ]
      )
