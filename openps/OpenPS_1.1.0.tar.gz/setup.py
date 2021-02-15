import codecs
from setuptools import setup

with codecs.open("README.md", 'r', encoding="utf-8") as f:
    long_description = "\n" + f.read()

setup(
   name='OpenPS',
   version='1.1.0',
   description='Open source plugin system.',
   long_description_content_type="text/markdown",
   long_description=long_description,
   license="Apache-2.0",
   dependency_links=["https://github.com/TheKruger/OpenPS"],
   author='TheKruger',
   keywords=["python", "plugin-system"],
   packages=['OpenPS']
)
