import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jsiter", # 
    version="1.0.3",
    author="HuJK",
    author_email="hu@hujk.eu.org",
    description="JavaScript flavor iterable",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HuJK/iterZ",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)