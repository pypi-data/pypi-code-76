#!/usr/bin/env/python

import setuptools

with open("README.md", "r", encoding='utf-8') as readme:
    long_description = readme.read()


setuptools.setup(
      name="clossh",
      version="0.0.1",
      description="A simple and lightweight clustering library based on the ssh protocol.",
      long_description=long_description,
      long_description_content_type="text/markdown",
      author="Guillaume Macneil",
      url="https://github.com/MetallicSquid/clossh",
      packages=setuptools.find_packages(),
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
            "Operating System :: Unix",
      ],
)
