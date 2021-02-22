import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="serverhttp", # Replace with your own username
    version="1.7.1",
    author="Allen",
    author_email="allen.haha@hotmail.com",
    description="A simple HTTP Server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/allen546/serverhttp",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
