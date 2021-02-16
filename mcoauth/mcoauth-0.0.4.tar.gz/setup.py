import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mcoauth", # Replace with your own username
    version="0.0.4",
    author="TheUltimateGuide",
    author_email="theultimateguideofficial@gmail.com",
    description="A small package to use MCOauth",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MySixSenses/MCOauth",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[
    'aiohttp'
    ]
)