import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="enimie",
    version="1.1.1",
    description="It for wordlist attacks",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/kavindunimesh/enimie",
    author="kavindu nimesh",
    author_email="k.nimesh.kn@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["enimie"],
    include_package_data=True,
    install_requires=["requests","argparse"],
    entry_points={
        "console_scripts": [
            "enimie=enimie.__main__:main",
        ]
    },
)
