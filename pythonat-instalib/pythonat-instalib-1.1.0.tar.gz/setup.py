import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pythonat-instalib",
    version="1.1.0",
    description="Read the latest Real Python tutorials",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Pythonat.com / dotslashhack.io",
    author_email="nasser@dotslashhack.io",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["pythonatinstalib"],
    include_package_data=True,
    install_requires=["selenium", "webdriver-manager","os","sys","wget","time","pynput"],
    entry_points={
        "console_scripts": [
            "pyinstalib=pythonatinstalib.__main__:main",
        ]
    },
)