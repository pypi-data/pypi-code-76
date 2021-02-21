import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name = "Ghidora",
    version = "0.0.1",
    author = "Jay Rank",
    author_email = "rank01jay01@gmail.com",
    description = "An abstract python library for calculating time complex math function.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/RankJay/Ghidora",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = ">=3.6",
)