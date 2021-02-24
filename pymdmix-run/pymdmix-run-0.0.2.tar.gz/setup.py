#!/usr/bin/env python3

from setuptools import setup


def getRequirements():
    requirements = []
    with open("requirements.txt", "r") as reqfile:
        for line in reqfile.readlines():
            requirements.append(line.strip())
    return requirements


def getVersion():
    return "0.0.2"


setup(
    python_requires=">=3.8",
    name="pymdmix-run",
    version=getVersion(),
    license="MIT",
    description="pymdmix plugin for command interpreter",
    author="ggutierrez-bio",
    author_email="",
    url="https://github.com/ggutierrez-bio/mdmix4/pymdmix-run",
    packages=["pymdmix_run"],
    install_requires=getRequirements(),
    classifiers=['Development Status :: 3 - Alpha'],
    scripts=["bin/mdmix-run"],
)
