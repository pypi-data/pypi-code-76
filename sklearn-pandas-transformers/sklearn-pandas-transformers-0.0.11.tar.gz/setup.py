import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sklearn-pandas-transformers",
    version="0.0.11",
    author="Thibault Blanc",
    # author_email="author@example.com",
    description=
    "A Package to use pandas DataFrame in sklearn pipeline. And others useful works to use sklearn pipeline in non usual way.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/thibaultB/transformers",
    install_requires=[
        "pandas>=0.24.2", "scikit-learn==0.23.2", "pytest>=6.0.1", "pylint>=2.6.0", "pytest-cov>=2.10.1", "coverage",
        "yapf"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)