import setuptools

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="simio",
    version="0.5.1",
    author="Nikita Zavadin",
    author_email="zavadin142@gmail.com",
    description="Small, simple and async web framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache 2.0",
    url="https://github.com/RB387/Simio",
    packages=setuptools.find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Framework :: AsyncIO",
        "License :: OSI Approved :: Apache Software License",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "simio=simio.cli.selector:select_action",
        ]
    },
)
