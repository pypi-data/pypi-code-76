from setuptools import find_packages, setup

from pathlib import Path
from os import path
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name='mt2gf',
    version='0.1.2',
    author='Yann Mentha',
    author_email="yann.mentha@gmail.com",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/ymentha14/mturk2gform",
    packages = find_packages(),
    license='MIT',
    python_requires='>=3.6',
    install_requires= Path("requirements.txt").read_text().splitlines(),
)
