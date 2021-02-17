import setuptools

from rhksm4._version import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rhksm4",
    version=__version__,
    author="Mirco Panighel",
    author_email="panighel@iom.cnr.it",
    description="A python package to read and parse .sm4 files from RHK Technology.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/rhksm4/rhksm4",
    license="MIT",
    packages=setuptools.find_packages(exclude=["test_files"]),
    install_requires=[
        "numpy",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)
