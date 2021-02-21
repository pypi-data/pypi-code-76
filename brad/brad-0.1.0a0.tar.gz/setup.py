from setuptools import find_packages, setup

setup(
    name="brad",
    version="0.0.0a1",
    description="Brad is a Python package for Bootstrap, permutation tests and other resampling functions.",
    author="tcbegley",
    author_email="tomcbegley@gmail.com",
    url="https://github.com/tcbegley/brad",
    package_dir={"": "src"},
    packages=find_packages("src"),
    install_requires=[
        "numpy>=1.18.0,<2.0.0",
        "scikit-learn>=0.24.0",
        "scipy>=1.4.1,<2.0.0",
    ],
    python_requires=">=3.7,<4.0",
    extras_require={
        ':python_version < "3.8"': ["importlib_metadata>=3.4.0,<4.0.0"]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
    ],
)
