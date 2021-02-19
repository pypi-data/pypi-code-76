import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="slidetemplater",  # Replace with your own username
    version="0.0.3",
    author="Stephen Brown",
    author_email="steve@slidetemplater.com",
    description="A client API for slidetemplater.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/evolvedlight/slideplater-python",
    packages=['slidetemplater'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
