import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="coloredterm",
    version="0.1.3",
    author="Hostedposted",
    author_email="hostedpostedsite@gmail.com",
    description="Color the text in your terminal.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hostedposted/coloredterm",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ],
    install_requires=["Pillow"],
    python_requires='>=2.7',
)