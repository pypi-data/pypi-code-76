from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Extraction most important keywords from any website'
LONG_DESCRIPTION = 'A package that allows to conclude what the website is for and its aim according to the extracted words.'

# Setting up
setup(
    name="summarext",
    version=VERSION,
    author="elvinaqa (Elvin Aghammadzada)",
    author_email="<elvinagammed@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['networkx==2.4',
                      'pandas==1.0.3',
                      'Flask==1.0.2',
                      'gensim==3.8.3',
                      'requests==2.23.0',
                      'keybert==0.1.3',
                      'matplotlib==3.3.0',
                      'beautifulsoup4==4.9.3'],
    keywords=['python', 'keyword', 'extract', 'keyword extraction', 'keyword summarization', 'scraping'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
