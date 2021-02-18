import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="htutil",
    version="0.1.0",
    author="117503445",
    author_email="t117503445@gmail.com",
    description="HaoTian's Python Util",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/117503445/htutil",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=['elasticsearch']
)
