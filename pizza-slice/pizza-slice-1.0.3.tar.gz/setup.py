from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="pizza-slice",
    version="1.0.3",
    description="A Python package to get weather reports for any location.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/nikhilkumarsingh/weather-reporter",
    author="Kakada Ly",
    author_email="ly103399@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["pizza_slice"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "pizza-slice=pizza_slice.run:main",
        ]
    },
)