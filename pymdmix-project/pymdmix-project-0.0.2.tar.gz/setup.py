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
    name="pymdmix-project",
    version=getVersion(),
    description="pymdmix project plugin",
    author="ggutierrez-bio",
    author_email="",
    url="https://github.com/ggutierrez-bio/mdmix4/pymdmix-project",
    data_files=[("pymdmix", ["defaults/pymdmix_project.yml"])],
    packages=["pymdmix_project"],
    install_requires=getRequirements(),
)
