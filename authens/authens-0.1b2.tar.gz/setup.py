import setuptools

with open("README.md", "r") as file:
    long_description = file.read()


setuptools.setup(
    name="authens",
    version="0.1b2",
    author="Klub Dev ENS",
    author_email="klub-dev@ens.fr",
    description="CAS Authentication at the ENS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.eleves.ens.fr/klub-dev-ens/authens",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires=">=3.5",
    install_requires=["Django>=2.2", "python-ldap>=3,<4", "python-cas>=1.5,<2"],
)
