from pathlib import Path
from setuptools import setup

with open(Path(__file__).parent / "README.md") as f:
    README = f.read()

setup(
    name="halfling",
    version="0.1.3",
    description="Small C/++ build system written in Python.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/aloebs29/halfling",
    author="Andrew Loebs",
    license="MIT",

    packages=["halfling"],
    include_package_data=True,
    install_requires=["toml"],
    entry_points={
        "console_scripts": [
            "halfling = halfling.main:run",
        ]
    },
)
