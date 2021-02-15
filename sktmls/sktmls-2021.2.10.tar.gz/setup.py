import setuptools


def load_long_description():
    with open("README.md", "r") as f:
        long_description = f.read()
    return long_description


def get_version():
    with open("sktmls/__init__.py", "r") as f:
        for line in f.readlines():
            if line.startswith("__version__"):
                return line.split('"')[1]
        else:
            raise TypeError("NO SKTMLS_VERSION")


setuptools.setup(
    name="sktmls",
    version=get_version(),
    author="SKTMLS",
    author_email="mls@sktai.io",
    description="MLS SDK",
    long_description=load_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/sktaiflow/mls-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.19.4,<1.20",
        "catboost>=0.24.3,<0.25.0",
        "joblib",
        "lightgbm>=2.3.1,<2.4.0",
        "pandas>=1.1.1,<1.2.0",
        "pytz",
        "requests",
        "scikit-learn>=0.23.2,<0.24",
        "scipy>=1.4.1,<1.5.0",
        "xgboost>=1.2.1,<1.3",
        "python-dateutil",
        "matplotlib>=3.2.1,<3.3",
        "tqdm>=4.51.0",
        "boto3",
        "ConfigSpace<=0.4.10",
        "cryptography>=3.2.1",
        "cython",
        "dask>=2.6.0",
        "distributed>=2.6.0",
        "fastparquet==0.4.1",
        "gluoncv>=0.5.0,<0.9.0",
        "graphviz<0.9.0,>=0.8.1",
        "mxnet<2.0.0",
        "networkx>=2.3,<3.0",
        "paramiko>=2.4",
        "Pillow>=8.0.1",
        "psutil>=5.7.3",
        "pyarrow>=2.0.0",
        "scikit-optimize",
        "tornado>=6.1",
    ],
)
