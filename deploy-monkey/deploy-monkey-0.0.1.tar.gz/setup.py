import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="deploy-monkey",
    version="0.0.1",
    author="Tino de Bruijn",
    author_email="tino@solarmonkey.nl",
    description="Currently to prevent dependency-confusion. Aim to open source later",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/solarmonkey/deploy-monkey",
    packages=setuptools.find_packages(include=["monkey"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
