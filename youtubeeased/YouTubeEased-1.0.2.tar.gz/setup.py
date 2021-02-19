from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="YouTubeEased",
    version="1.0.2",
    description="A basic library which will give you a better and easier experience with youtube API",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="",
    author="Daniel Katz",
    author_email="",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows"
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["YouTubeEased"]
)
