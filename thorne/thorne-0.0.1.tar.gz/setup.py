import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="thorne",  # Replace with your own username
    version="0.0.1",
    author="Cis International",
    author_email="ofekbendavid9@gmail.com",
    description="Thorne for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ofsho/Thorne",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)