import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FileTransfer-LQR471814", # Replace with your own username
    version="0.1.1",
    author="LQR471814",
    author_email="bramblefern1013@gmail.com",
    description="A module that makes File Transfer a bit easier.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LQR471814/FileTransfer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)