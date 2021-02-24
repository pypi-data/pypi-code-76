import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("VERSION", "r", encoding="utf-8") as fh:
    version = fh.read()

setuptools.setup(
    name="Genx", # Replace with your own username
    version=version,
    author="$x",
    author_email="scxlmtkl@gmail.com",
    description="A small package to get Discord Nitro",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ICExFS/GenX",
    project_urls={
        "Bug Tracker": "https://github.com/ICExFS/GenX/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)