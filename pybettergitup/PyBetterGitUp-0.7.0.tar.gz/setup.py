from setuptools import setup, find_packages
from PyBetterGitUp.version import __VERSION__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="PyBetterGitUp",
    version=__VERSION__,
    packages=find_packages(exclude=["tests"]),
    scripts=['PyBetterGitUp/bgitup.py'],
    install_requires=[
        'GitPython==3.1.7',
        'git-up==1.6.1',
        'colorama>=0.4.3',
        'gitversion==2.1.3'
    ],

    # Executable
    entry_points={
        'console_scripts': [
            'bgitup = bgitup:run'
        ]
    },

    # Metadata
    author="Edward Taylor",
    author_email="edweird06@users.noreply.github.com",
    description="A better package for git up",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/edweird06/BetterGitUp",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
