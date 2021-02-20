#!/usr/bin/env python3

from setuptools import setup


def getRequirements():
    requirements = []
    with open("requirements.txt", "r") as reqfile:
        for line in reqfile.readlines():
            requirements.append(line.strip())
    return requirements


def getVersion():
    return "4.0.2"


setup(
    python_requires=">=3.8",
    name="pymdmix-core",
    zip_safe=False,
    version=getVersion(),
    description="Molecular Dynamics with organic solvent mixtures setup and analysis",
    author="ggutierrez-bio",
    author_email="",
    url="https://github.com/ggutierrez-bio/mdmix4",
    packages=["pymdmix_core", "pymdmix_core.plugin"],
    inlcude_package_data=True,
    data_files=[("pymdmix", ["defaults/pymdmix_core.yml"])],
    scripts=["bin/mdmix"],
    install_requires=getRequirements(),
)
