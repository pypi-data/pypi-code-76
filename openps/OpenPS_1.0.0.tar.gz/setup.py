import codecs
from setuptools import setup

with codecs.open("README.md", 'r', encoding="utf-8") as f:
    long_description = "\n" + f.read()

setup(
   name='OpenPS',
   version='1.0.0',
   description='Open source plugin system.',
   long_description_content_type="text/markdown",
   long_description=long_description,
   author='TheKruger',
   keywords=["python", "plugin-system"],
   packages=['OpenPS']
)
