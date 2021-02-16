from setuptools import setup

with open('README.md', encoding='utf-8') as f:
    README = f.read()

setup(
    name="justgood",
    version="2.2.0",
    description="Sample request for api.imjustgood.com please visit webpage imjustgood.com for more details",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/goodop/api-imjustgood.com",
    author="Yoshino",
    author_email="admin@imjustgood.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["justgood"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
)