#!/usr/bin/env python
import re

from setuptools import setup  # type: ignore


METADATA = {}
with open("docutils_tinyhtml/__init__.py", "r") as info:
    METADATA = dict(re.findall(r'__([a-z_]+)__ = "([^"]+)"', info.read()))

def doc():
    """Return README.rst content."""
    with open('README.rst', 'r') as readme:
        return readme.read().strip()


setup(
    name="docutils-tinyhtmlwriter",
    version=METADATA['version'],
    description="Docutils Writer producing Tiny HTML",
    author=METADATA['author_name'],
    author_email=METADATA['author_email'],
    url=METADATA['url'],
    packages=['docutils_tinyhtml'],
    package_data={'': ['py.typed', 'tiny-writer.css']},
    scripts=['rst2html-tiny', 'md2html-tiny'],
    license="BSD",
    long_description=doc(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Natural Language :: Czech",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Documentation",
        "Topic :: Software Development :: Documentation",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Markup",
        "Topic :: Utilities"],
    requires=['docutils (>= 0.12)'],
    extra_requires=['m2r', 'Pygments'],
    install_requires=['docutils >= 0.12']
)
