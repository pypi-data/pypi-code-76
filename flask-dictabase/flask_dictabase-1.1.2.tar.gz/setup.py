from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

packages = ['flask_dictabase']

setup(
    name="flask_dictabase",

    version="1.1.2",
    # 1.1.2 - Added .GetItem()
    # 1.1.0 - Added .Remove() and .PopItem()
    # 1.0.16 - Issues with .Set() not committing to db ?
    # 1.0.12 - Added with self.db.lock and WaitForTransactionsToComplete to FindOne and FindAll to prevent error "sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) database is locked"
    # 1.0.10 - Added BaseTable.app so you can easily access the app from inside a BaseTable object method
    # 1.0.9 - Added helper methods to BaseTable: Append() and SetItem()
    # 1.0.8 - New(), FindOne() and FindAll() can now pass str or class as first arg
    # 1.0.7 - Added BaseTable Set/Get methods to help deal with unsuported db types

    packages=packages,
    install_requires=[
        'flask',
        'dataset',
    ],

    author="Grant miller",
    author_email="grant@grant-miller.com",
    description="A dict() like interface to your database.",
    long_description=long_description,
    license="PSF",
    keywords="grant miller flask database",
    url="https://github.com/GrantGMiller/flask_dictabase",  # project home page, if any
    project_urls={
        "Source Code": "https://github.com/GrantGMiller/flask_dictabase",
    }

)
