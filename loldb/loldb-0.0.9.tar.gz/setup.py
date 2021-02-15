import setuptools

# read the readme.md file and
# add it as the
# long description of our package


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()




setuptools.setup(
    name="loldb",  # Replace with your own username
    version="0.0.9",
    author="P Pranav Baburaj",
    author_email="code-roller@googlegroups.com",
    description="A simple json database and other utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pranavbaburaj/lol",
    packages=setuptools.find_packages(),
    install_requires=['dicttoxml', "clint", "click"],
    entry_points={"console_scripts": ['lol = cli.cli:main']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)