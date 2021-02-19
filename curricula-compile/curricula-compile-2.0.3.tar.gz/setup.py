import importlib.util
from setuptools import setup, find_packages
from pathlib import Path


root = Path(__file__).absolute().parent

with root.joinpath("README.md").open() as fh:
    long_description = fh.read()

name = "curricula_compile"
spec = importlib.util.spec_from_file_location(name, str(root.joinpath(name, "version.py")))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

setup(
    name="curricula-compile",
    version=module.version,
    description="An assignment bundler for the Curricula ecosystem",
    url="https://github.com/curriculagg/curricula",
    author="Noah Kim",
    author_email="noahbkim@gmail.com",

    # Extra
    long_description=long_description,
    long_description_content_type="text/markdown",

    # Python
    python_requires=">=3.9",

    # Packaging
    packages=find_packages(),
    package_data={"curricula_compile": ["schema/*.json", "template/**/*.md", "template/**/*.html"]},
    include_package_data=True,
    zip_safe=False,
    install_requires=["jinja2", "jsonschema", f"curricula=={module.version}"])
