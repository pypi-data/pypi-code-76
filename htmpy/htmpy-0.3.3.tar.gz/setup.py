import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="htmpy",
    version="0.3.3",
    author="riioze",
    author_email="riioze0@gmail.com",
    description="Package to create automatically webpages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/riioze/htmpy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)