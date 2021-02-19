from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name = 'curva',
    author = 'origamizyt',
    author_email = 'zhaoyitong18@163.com',
    version = '1.0',
    python_requires = '>=3',
    install_requires = ['ecdsa', 'PyCryptodome'],
    description = 'Simple library for ECIES with AES and HKDF.',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'http://github.com/origamizyt/curva',
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages = find_packages()
)