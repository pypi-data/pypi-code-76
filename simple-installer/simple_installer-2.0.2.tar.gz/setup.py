import setuptools

with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

requirements = []
with open('requirements.txt', 'r') as fh:
    for line in fh:
        requirements.append(line.strip())


setuptools.setup(
    name="simple_installer",
    version="2.0.2",
    author="Dmitrii Shevchenko",
    author_email="dmitrii.shevchenko96@gmail.com",
    description="Extendable installer for latest Github repository release.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/S0nic014/simple_installer",
    install_requires=requirements,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6"
)
