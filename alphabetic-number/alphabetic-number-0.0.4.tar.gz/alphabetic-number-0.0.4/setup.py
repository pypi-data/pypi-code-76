import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="alphabetic-number",
    version="0.0.4",
    author="Danila Panteleev",
    author_email="pont131995@gmail.com",
    description="Convert number to alphabetical from",
    long_description=long_description,
    url="https://github.com/danila-panteleev/alphabetic-number",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)