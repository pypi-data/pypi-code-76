import setuptools
import requests

with open("README.md", "r") as fh:
    long_description = fh.read()

r = requests.get("https://pypi.org/pypi/pyoinformatics/json")
version = r.json()["info"]["version"].split(".")
patch_version = str(int(version[-1]) + 1)
if patch_version == "9":
    patch_version = "0"
    version[1] = str(int(version[1]) + 1)

setuptools.setup(
    name="pyoinformatics",  # Replace with your own username
    version=".".join(version[:-1] + [patch_version]),
    author="Wytamma Wirth",
    author_email="wytamma.wirth@me.com",
    description="A simple bioinformatics package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Wytamma/pyoinformatics",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
