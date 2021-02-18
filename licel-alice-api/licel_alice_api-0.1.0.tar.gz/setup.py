from os import path

from setuptools import find_packages, setup

# read the contents of your README file
project_dir = path.abspath(path.dirname(__file__))
with open(path.join(project_dir, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="licel_alice_api",
    packages=find_packages(),
    version="0.1.0",
    description="Alice API",
    author="Licel",
    license="MIT",
    install_requires=["requests", "python-keycloak"],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
