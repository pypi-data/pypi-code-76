"""
    This is the setup file for the PIP minecraft_learns package.

    Written By: Kathryn Lecha and Nathan Nesbitt
    Date: 2021-02-02
"""

from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="minecraft_stores",
    version="0.0.5",
    description=
        "Python library for saving minecraft game data to disk.",
    url="https://github.com/Nathan-Nesbitt/Minecraft_Store",
    author=(
        "Carlos Rueda Carrasco, Kathryn Lecha, Nathan Nesbitt," + 
        "Adrian Morillo Quiroga"),
    packages=[
        "minecraft_stores"
    ],
    install_requires=[
        "pandas",
        "wheel",
        "nest_asyncio",
        "pytest-asyncio",
        "pytest"
    ],
    zip_safe=False,
    long_description=long_description,
    long_description_content_type='text/markdown'
)
