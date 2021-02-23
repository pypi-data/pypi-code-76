import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "texta-face-analyzer",
    version = read("VERSION").strip(),
    author = "TEXTA",
    author_email = "info@texta.ee",
    description = ("TEXTA's interface for identiying and comparing facial encodings."),
    license = "GPLv3",
    packages = ["texta_face_analyzer"],
    data_files = ["VERSION", "requirements.txt", "README.md", "LICENSE"],
    long_description = read("README.md"),
    long_description_content_type="text/markdown",
    url="https://git.texta.ee/texta/texta-face-analyzer-python",
    install_requires = read("requirements.txt").split("\n"),
    include_package_data = True
)
