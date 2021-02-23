from setuptools import setup, find_packages

with open("README.md", "r") as file_:
    long_description = file_.read()

setup(
    name="declair",
    version="0.1.4",
    author="Krzysztof Cybulski",
    author_email="declair@kcyb.eu",
    description="Package for declarative hyperparameter search experiments.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/k-cybulski/declair",
    packages=find_packages(exclude=('tests', 'examples')),
    python_requires='>=3.5',
    license='EUPL-1.2-or-later',
    install_requires=['sacred>=0.8.2', 'hyperopt>=0.2.4', 'pymongo', 'pyyaml', 'tblib', 'GitPython', 'wrapt'],
    entry_points={
        "console_scripts": [
            "declair-omniboard = declair.bin.declair_omniboard:main",
            "declair-execute = declair.bin.declair_execute:main"
        ]
    }
)
