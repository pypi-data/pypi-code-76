from setuptools import setup

with open("README.md","r") as fh:
    long_description = fh.read()

setup(
    name="Easy-QLearning",
    version="1.0.1",
    description="Simplify the creation of QLearning",
    py_modules=["EQL"],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires = [
        "numpy ~= 1.19",
    ],
    extras_require={
        "dev":[
            "pytest>=3.7",
        ],
    },
    url="https://github.com/ProfesseurIssou/EQL",
    author="Hamidou Alix",
    author_email="alix.hamidou@gmail.com",
)