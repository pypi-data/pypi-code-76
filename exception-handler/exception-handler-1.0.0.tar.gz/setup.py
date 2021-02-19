__version__ = '1.0.0'

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name="exception-handler",
    version=__version__,
    author="Bruno Henrique de Paula",
    author_email="bruno.henriquy@gmail.com",
    description="Exception Handler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    url="https://github.com/PartyouPay/exception-handler.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
    zip_safe=False
)
