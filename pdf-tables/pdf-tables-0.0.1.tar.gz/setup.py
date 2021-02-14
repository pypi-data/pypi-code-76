from setuptools import setup, find_packages
#import pathlib
#HERE = pathlib.Path(__file__).parent
#LONG_DESCRIPTION = (HERE / "README.md").read_text()
#LONG_DESC_TYPE = "text/markdown"

setup(
    name = "pdf-tables",
    packages=find_packages(),
    version = "0.0.1",
    description = "Pull tables from pdfs",
    author="Jason Trigg",
    license="MIT",
    author_email="jasontrigg0@gmail.com",
    url="https://github.com/jasontrigg0/pdf-tables",
    scripts=["pdf-tables/pdftables"],
    install_requires=[
        "numpy",
        "pandas",
        "pdfplumber",
        "scikit-image",
        "tesserocr",
        "matplotlib",
        "pillow",
        "opencv-python"
    ],
)
