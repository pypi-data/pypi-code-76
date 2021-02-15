import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="finder_string",
    version="0.1.1",
    author="Raymond46",
    author_email="maks.sokol.2015@inbox.ru",
    description="Search for a string in all possible files in the directory. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vander00/Finder-in-files.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>3.6',
)