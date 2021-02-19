import setuptools

requirements = []
with open('requirements.txt', 'r') as fh:
    for line in fh:
        requirements.append(line.strip())

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="r2api",
    version="0.1.8",
    author="Benyakir Horowitz",
    author_email="benyakir.horowitz@gmail.com",
    description="A small package to translate an Italian recipe and its units into English and imperial units using Google Translate",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/benyakirten/r2api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha"
    ],
    python_requires='>=3.6',
    install_requires = requirements
)