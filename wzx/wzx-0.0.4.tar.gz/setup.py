import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wzx",
    version="0.0.4",
    author="Zhenxin (Jason) Wang",
    author_email="wzhx.cc@gmail.com",
    description="util",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://zhenesis.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)