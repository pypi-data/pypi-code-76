import setuptools

with open("README.txt", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easycolors", # Replace with your own username
    version="1.0.4",
    author="Sjoerd Vermeulen",
    author_email="sjoerd@marsenaar.com",
    description="A simple tool for convinient rgb-tuple use",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=['easycolors'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
