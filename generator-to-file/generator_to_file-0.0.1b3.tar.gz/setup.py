import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="generator_to_file", # Replace with your own username
    version="0.0.1b3",
    author="Paris Liu",
    author_email="paris0120@gmail.com",
    description="Business research tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/paris0120/generator_to_file",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
