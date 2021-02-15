from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="pizza-slice",
    version="1.0.5",
    description="A Python package to get weather reports for any location.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/lkakada/Prime-Number",
    author="Kakada Ly",
    author_email="ly103399@gmail.com",
    license="MIT",
    packages=find_packages(where='src'),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "pizza-slice=pizza_slice.run:main",
        ]
    },
)