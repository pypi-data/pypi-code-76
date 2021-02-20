from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    dependencies = [line for line in f]

with open("requirements-dev.txt") as f:
    dev_dependencies = [line for line in f]

setup(
    name="monkey_vision",
    version="0.1.0",
    author="Valdio Veliu <Valdio Veliu>",
    author_email="valdioveliu@gmail.com",
    url="https://github.com/monkey-cli/monkey_vision",
    description="Computer vision image analyses for monkey screenshots.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=dependencies,
    extras_require={"dev": dev_dependencies},
)
