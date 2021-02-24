from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'String analysis package.'
LONG_DESCRIPTION = 'A package that takes as input a string stream and a query word and returns which word ' \
                   'on the stream is most similar to the query.'

# Setting up
setup(
    name="ramon-stringanalysis",
    version=VERSION,
    author="Ramon Duraes",
    author_email="ramongduraes@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'string', 'take'],
    classifiers=[
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
