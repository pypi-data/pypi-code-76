from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='elasticdb',
    packages=find_packages(include=['statebasedml']),
    version='0.0.1',
    author='Wesley Belleman',
    author_email="bellemanwesley@gmail.com",
    description="Use Elasticsearch as a database.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bellemanwesley/elasticdb",
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)