import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nepox",
    version="0.0.1",
    author="Moris Doratiotto",
    author_email="moris.doratiotto@gmail.com",
    description="Script to create a new Python project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mortafix/Nepox",
    packages=setuptools.find_packages(),
    install_requires=["argparse"],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.6",
    keywords=["project", "venv", "create"],
    entry_points={"console_scripts": ["nepox=nepox.nepox:main"]},
)
