import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fetchcreds", # Replace with your own username
    version="0.0.1",
    author="Alexandr Moskalev",
    author_email="alexandr@reveliolabs.com",
    description="A very small wrapper-package for bitwarden_rs credentials retrieval",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/opencareer/security",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)
