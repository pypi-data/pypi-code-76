import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cerami",
    version="0.3.4",
    author="Zac Brown",
    author_email="gummybuns@protonmail.com",
    description="A Dynamodb ORM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    url="https://github.com/gummybuns/cerami",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'boto3',
        'python-dateutil',
    ],
)
