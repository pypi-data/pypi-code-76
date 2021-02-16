import os
import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="acdh_uri-norm-rules", # Replace with your own username
    version="2.0.0",
    author="Mateusz Żółtak",
    author_email="mzoltak@oeaw.ac.at",
    description="A set of URI normalization rules used by the ACDH",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/acdh-oeaw/UriNormRules",
    packages=setuptools.find_packages(),
    package_data={'AcdhUriNormRules': ['rules.json']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True
)
