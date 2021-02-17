import setuptools

with open("autoBoostcamp/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autoBoostcamp",
    version="3.7",
    author="datadriven42",
    author_email="datadriven42@gmail.com",
    description="A moudule for self-authentication",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "selenium",
        "chromedriver_autoinstaller"
    ],
    python_requires='>=3.6',
)