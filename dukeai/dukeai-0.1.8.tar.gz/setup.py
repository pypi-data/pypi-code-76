import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
                    name="dukeai",
                    version="0.1.8",
                    author="shubham kothari",
                    author_email="shubham@duke.ai",
                    description="Dukeai Development Package",
                    long_description=long_description,
                    url="https://duke.ai",
                    install_requires=['boto3', 'requests'],
                    packages=setuptools.find_packages(),
                    classifiers=[
                                    "Programming Language :: Python :: 3",
                                    "License :: OSI Approved :: MIT License",
                                    "Operating System :: OS Independent",
                                ],
                )

# pip install twine
# python setup.py sdist
# twine upload dist/*
