from setuptools import setup, find_packages

classifiers = [
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
]

setup(
    name = "keyvalue_database_replit",
    version = "0.0.1",
    description = "Key Value DataBase",
    long_description = f"New version of keyvalue_database module that is designed to work on repl.it",
    author = "Miguel Merheb/ Ahmad Zaaroura",
    author_email = "ahmad.zaaroura.123@gmail.com",
    url = "",
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