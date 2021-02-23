import os
import re
import setuptools


def read_file(path):
    with open(os.path.join(os.path.dirname(__file__), path)) as fp:
        return fp.read()


def _get_version_match(content):
    # Scan package __init__.py for a __version__ line
    # and grab the output literal
    regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
    version_match = re.search(regex, content, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def get_version(path):
    return _get_version_match(read_file(path))


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="lilies",
    version=get_version(os.path.join("lilies", "__init__.py")),
    description="A tool for creating colorful, formatted command line output",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mrz1988/lilies",
    license="MIT",
    author="Matt Zychowski",
    author_email="mrz2004@gmail.com",
    packages=setuptools.find_packages(),
    package_data={"lilies.style.palettes": ["*.json"]},
    install_requires=[
        "colorama",
        "future",
        'importlib_resources; python_version < "3.7"',
    ],
    python_requires=">=3.5",
)
