import setuptools


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="amitool",
    version="0.1.2",
    author="ccmldl",
    author_email="1738407610@qq.com",
    description="create session and redis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ccmldl/AmiTools",
    packages=setuptools.find_packages(),
    install_requires=["loguru==0.5.3","pyodbc==4.0.30","redis==3.5.3","SQLAlchemy==1.3.23"]
)