import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kubert",
    version="0.0.5",
    author="James Jones",
    author_email="jam.jones@f5.com",
    description="A Python Kubernetes API client designed to for making easy to register callbacks for watches",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nginx-architects/kubert",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Freely Distributable",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)