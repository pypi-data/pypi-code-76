import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ytproofreading",
    version="1.4",
    author="6ast1an979",
    author_email="6ast1an979@gmail.com",
    description="A python module to use the proofreading support api of Yahoo! japan",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/6ast1an979/ytproofreading",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
