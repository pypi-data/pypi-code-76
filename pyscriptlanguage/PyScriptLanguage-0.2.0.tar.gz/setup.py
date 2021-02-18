from setuptools import setup

README = open("README.md", "r").read()

setup(
    name = 'PyScriptLanguage',
    version = '0.2.0',
    description = 'A simple Scripting Language',
    long_description=README,
    long_description_content_type="text/markdown",
    packages = ['pyscript'],
    entry_points = {
        'console_scripts': [
            'pyscript = pyscript.__main__:main'
        ]
    })
