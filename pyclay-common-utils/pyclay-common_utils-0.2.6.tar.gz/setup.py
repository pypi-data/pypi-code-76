from setuptools import setup, find_packages
import common_utils

packages = find_packages(
        where='.',
        include=['common_utils*']
)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyclay-common_utils',
    version=common_utils.__version__,
    description='Common utilities for convenience.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cm107/common_utils",
    author='Clayton Mork',
    author_email='mork.clayton3@gmail.com',
    license='MIT License',
    packages=packages,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'Cython>=0.29.14',
        'opencv-python>=4.1.1.26',
        'numpy>=1.17.2',
        'requests>=2.22.0',
        'pylint>=2.4.2',
        'tqdm>=4.36.1',
        'scipy>=1.4.1',
        'imgaug>=0.3.0',
        'PyYAML>=5.3.1',
        'pyclay-logger==0.2'
    ],
    python_requires='>=3.7'
)