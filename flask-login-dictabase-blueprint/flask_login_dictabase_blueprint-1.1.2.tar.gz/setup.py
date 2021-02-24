from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

packages = ['flask_login_dictabase_blueprint']

setup(
    name="flask_login_dictabase_blueprint",

    version="1.1.2",
    # 1.1.2 - Added userOnly option to Menu
    # 1.1.0 - Added menu module
    # 1.0.10 - Added RenderTemplate decorator to help customizing templates
    # 1.0.9 - added SignedIn decorator, triggers callback when a user signs in

    packages=packages,
    install_requires=[
        'flask',
        'flask_login',
        'flask_dictabase',
    ],

    setup_requires=['setuptools_scm'],
    package_data={
        'flask_login_dictabase_blueprint.templates': ['*'],
    },  # All files from folder A
    include_package_data=True,

    author="Grant miller",
    author_email="grant@grant-miller.com",
    description="A simple flask blueprint for managing users",
    long_description=long_description,
    license="PSF",
    keywords="grant miller flask database flask_dictabase flask_login blueprint",
    url="https://github.com/GrantGMiller/blueprint_flask_login_dictabase",  # project home page, if any
    project_urls={
        "Source Code": "https://github.com/GrantGMiller/blueprint_flask_login_dictabase",
    }

)
