from setuptools import setup, find_packages

classifiers = [
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
]

setup(
    name = "keyvalue_database",
    version = "0.0.81",
    description = "Key Value DataBase",
    long_description = f"This module allows you to create and save simple key-value database to do some tasks.\n You can check the source code in the github repo under project links.",
    author = "Ahmad Zaaroura",
    author_email = "ahmad.zaaroura.123@gmail.com",
    url = "https://github.com/AhmadZ1/Key-Value-DataBase",
    license = "MIT",
    classifiers = classifiers,
    keywords = 'DataBase',
    packages = find_packages(),
    python_requires = ">=3.6",
)


#python setup.py sdist bdist_wheel
#twine check dist/*
#twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

#username: asz07
#password: Ahmad.Z.1133

#Remember to change the version 