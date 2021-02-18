from setuptools import find_packages, setup

__version__ = "0.2.6"


def long_description():
    with open("README.md", "r") as f:
        long_desc = f.read()
    return long_desc


setup(
    name="gerridae",
    version=__version__,
    author="buglan",
    packages=find_packages(),
    description="a crawl framework just for fun",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    author_email="dev.buglan@gmail.com",
    python_requires=">=3.6",
    install_requires=["cssselect", "lxml", "aiohttp"],
    url="https://github.com/BUGLAN/gerridae",
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
)
