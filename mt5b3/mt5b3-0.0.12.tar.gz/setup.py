import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mt5b3",
    version="0.0.12",
    author="Paulo Andre L. de Castro",
    license='MIT', 
    author_email="paulo.al.castro@gmail.com",
    description="mt5b3 provides access to the B3 stock exchange to python programs through Metatrader and some Brazilian brokers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/paulo-al-castro/mt5b3/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)