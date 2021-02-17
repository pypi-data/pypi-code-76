import setuptools

import os

with open("README.md", "r") as fh:
    long_description = fh.read()

def read_requirements():
    """Parse requirements from requirements.txt."""
    reqs_path = os.path.join('.', 'install-requirements.txt')
    with open(reqs_path, 'r') as f:
        requirements = [line.rstrip() for line in f]
    return requirements

setuptools.setup(
    name="margo-parser", 
    version="0.0.3a0",
    author="Jake Kara",
    author_email="jake@jakekara.com",
    description="A notebook description language parser",
    url="https://github.com/jakekara.com/nbdl",
    packages=setuptools.find_packages(),
    install_requires=read_requirements(),
    # install_requires=[
    #     "lark-parser[regex]==0.10.0",
    #     "pyyaml"
    # ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    python_requires='>=3.6',
    package_data={'margo_parser': ['tokenizer/margo.lark']},
)