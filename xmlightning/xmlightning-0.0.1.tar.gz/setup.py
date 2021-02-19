import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xmlightning",
    version="0.0.1",
    author="hunterg3",
    author_email="hunterg123987@gmail.com",
    description="Allows you to create a simple and advanced xml parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/beanowonotanuwu/xmlightning",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
