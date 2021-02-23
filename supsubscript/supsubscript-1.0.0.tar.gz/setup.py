import setuptools

with open("README.txt", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="supsubscript", # Replace with your own username
    version="1.0.0",
    author="Sjoerd Vermeulen",
    author_email="sjoerd@marsenaar.com",
    description="A simple module for string conversion to super- and subscript",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=['supsubscript'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
