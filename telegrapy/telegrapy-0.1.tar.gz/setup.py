from setuptools import setup
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="telegrapy",
    version="0.1",
    description="Telegram Bot API",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/sudogene/telegrapy",
    author="sudogene",
    author_email="andywubby@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["telegrapy"],
    include_package_data=True,
    install_requires=["feedparser", "html2text"],
)
