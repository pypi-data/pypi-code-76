import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wundercell",
    version="0.0.1",
    author="hackwagon",
    author_email="hello@hackwagon.com",
    description="Wundercell package to extend the notebook environment",
    long_description=long_description,
    url="https://wundercell.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
      'requests',
      'pandas'
    ]
)