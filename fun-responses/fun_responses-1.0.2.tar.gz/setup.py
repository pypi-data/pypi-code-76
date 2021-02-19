import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fun_responses",
    version="1.0.2",
    author="Jason O'Donnell",
    author_email="void206551@gmail.com",
    description="An API for getting fun responses",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://void206551.dev/projects/fun-responses",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)