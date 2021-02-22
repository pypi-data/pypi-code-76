import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="multitrim",
    version="1.2.0",
    author="Kenji Gerhardt",
    author_email="kenji.gerhardt@gmail.com",
    description="A readtrimming and quality control pipeline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KGerhardt/multitrim",
    packages=setuptools.find_packages(),
    python_requires='>=3',
	entry_points={
        "console_scripts": [
            "multitrim=multitrim.multitrim:main",
        ]
    }
)