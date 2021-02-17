import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="napplib",
    version="0.3.34",
    author="Leandro Vieira",
    author_email="leandro@nappsolutions.com",
    description="Small lib with custom functions to handle with azure, napp hub and custom workflows",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leandrovieiraa/napplib.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests",
        "azure-storage-blob==2.1.0", 
        "tinydb", 
        "pandas", 
        "patool==1.12",
        "google-api-core==1.25.1",
        "google-api-python-client==1.12.8",
        "google-auth==1.25.0",
        "google-auth-httplib2==0.0.4",
        "google-auth-oauthlib==0.4.2",
        "googleapis-common-protos==1.52.0"
    ],
    package_data={"azure":["*"], "hub":["*"], "vtex":["*"], "shopify":["*"], "opabox":["*"], "mpms":["*"], "ftp":["*"]},
)
