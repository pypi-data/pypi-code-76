import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gb-automation-client",
    version="0.0.5",
    author="Emilia",
    author_email="emilia@gamebench.net",
    description="Python GameBench Automation (GBA) client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GameBench/gba-client-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
    ],
)
