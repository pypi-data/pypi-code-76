import importlib.util
from setuptools import setup, find_packages
from pathlib import Path


root = Path(__file__).absolute().parent

with root.joinpath("README.md").open() as fh:
    long_description = fh.read()

spec = importlib.util.spec_from_file_location(
    "curricula_grade_cpp",
    str(root.joinpath("curricula_grade_cpp", "version.py")))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

setup(
    name="curricula_grade_cpp",
    version=module.version,
    description="A set of grading addons specific to C++",
    url="https://github.com/curriculagg/curricula-grade-cpp",
    author="Noah Kim",
    author_email="noahbkim@gmail.com",

    # Extra
    long_description=long_description,
    long_description_content_type="text/markdown",

    # Python
    python_requires=">=3.9",

    # Packaging
    packages=find_packages(),
    package_data={"curricula_grade_cpp": [
        "include/*.hpp",
        "include/**/*.hpp",
        "gtest/*.cpp"]},
    include_package_data=True,
    zip_safe=False,
    install_requires=[f"curricula=={module.version}", f"curricula-grade=={module.version}"])

