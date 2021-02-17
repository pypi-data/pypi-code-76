from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='nutritranslate',
    packages=find_packages(include=['nutritranslate']),
    version='0.4.2',
    description='A service that translates and normalizes food nutrients',
    author='Renato Campos',
    author_email='renatoineeve@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ineeve/nutrients-translator",
    license='MIT',
    install_requires=[],
    python_requires='>=3.6'
)