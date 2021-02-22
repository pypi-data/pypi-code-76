# based on: https://packaging.python.org/tutorials/packaging-projects/  (as of 29.09.2019).

import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="signum",
    version="0.1.1",
    author="savetheginger",
    author_email="mysh995@gmail.com",
    description="NumPy-based signal data container tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/savetheginger/signum",
    packages=setuptools.find_packages(exclude=('examples',)),
    python_requires='>=3.7',
    install_requires=[
        'numpy>=1.16',
        'matplotlib'
    ],
    extras_require={
        'examples': ['notebook']  # jupyter notebook
    }
)
