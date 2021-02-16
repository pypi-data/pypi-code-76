import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    INSTALL_REQUIREMENTS = f.read().splitlines()

EXTRA_REQUIREMENTS = {
    'dev': [
        'pytest',
    ],
    'jwt': [
        'pyjwt'
    ],
    'google-auth': [
        'google-auth'
    ]
}

setuptools.setup(
    name="ntsvetanov-test-pypi",
    version="0.0.3",
    author="ntsvetanov",
    author_email="author@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ntsvetanov/ntsvetanov_test_pypi",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    install_requires=INSTALL_REQUIREMENTS,
    extras_require=EXTRA_REQUIREMENTS,
    python_requires='>=3.6',
)
