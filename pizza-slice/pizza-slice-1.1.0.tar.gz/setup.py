from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="pizza-slice",
    version="1.1.0",
    description="A Python package to get sum or subtraction for two values.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/lkakada/Prime-Number",
    author="Kakada Ly",
    author_email="ly103399@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    include_package_data=True,
    install_requires=["Flask==1.0.2"],
    packages = ['calc'],
)