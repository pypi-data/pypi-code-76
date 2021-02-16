import setuptools
from setuptools.command.develop import develop
from setuptools.command.install import install

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


class PostDevelopCommand(develop):
    def run(self):
        develop.run(self)
        import pysisl
        pysisl.loads("{}")


class PostInstallCommand(install):
    def run(self):
        install.run(self)
        import pysisl
        pysisl.loads("{}")


setuptools.setup(
    name="pysisl",
    version="0.0.2",
    author="Oakdoor",
    author_email="oakdoor.support@paconsulting.com",
    description="A python library for serialising and deserialising SISL (Simple Information Serialization Language)",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/oakdoor/pysisl",
    project_urls={
        'Project': 'https://oakdoor.io',
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    setup_requires=['ply', 'jsonschema'],
    install_requires=['ply', 'jsonschema'],
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
    python_requires='>=3.6'
)
