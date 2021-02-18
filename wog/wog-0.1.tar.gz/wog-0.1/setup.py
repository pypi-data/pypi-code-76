from setuptools import setup
setup(
    name='wog',
    version='0.1',
    description='World Of Games - Have a fun with some little games.',
    py_modules=["Live", "Game", "GuessGame", "MemoryGame", "CurrencyRouletteGame", "MainGame", "currency_converter",
                "random", "time"],
    package_dir={'': 'src'},
)

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wog",
    version="0.1",
    author="Nissim Museri",
    author_email="nissim34@gmail.com",
    description="A Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nissimuseri",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)