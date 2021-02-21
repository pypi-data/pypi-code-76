from setuptools import setup, find_packages

with open("ftest/version.py") as f:
    version = f.read()

_, version = version.split("=")
version = version.strip()

version = version[1:-1]

with open("README.md") as f:
    long_description = f.read()

setup(
    name="ftest",
    description="Integration Test Framework for Formula Student Lisboa",
    version=version,
    author="Gonçalo Silva, Joao Freitas",
    author_email="goncalo.acbs@gmail.com, joaj.freitas@gmail.com",
    license="GPLv3",
    url="https://gitlab.com/projectofst/software10e",
    #download_url="https://gitlab.com/joajfreitas/fcp-core/-/archive/v0.32/fcp-core-v0.29.tar.gz",
    packages=find_packages(),
    entry_points={"console_scripts": ["ftest = ftest.__main__:main",],},
    install_requires=["fcp", "colored", "click", "termcolor", "loguru", "result==0.6.0-rc.1"],
    long_description=long_description,
    long_description_content_type="text/markdown"
)
