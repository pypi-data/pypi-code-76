import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kved_finder",
    version="v2.4",
    author="elem3ntary",
    author_email="impr0digg@gmai.com",
    description="A package for finding kved tree",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/elem3ntary/kved_finder",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
)
