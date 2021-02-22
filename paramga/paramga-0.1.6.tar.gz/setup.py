import setuptools
import pathlib

here = pathlib.Path(__file__).parent.resolve()

with open("README.md", "r") as fh:
    long_description = fh.read()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setuptools.setup(
    name="paramga",
    version="0.1.6",
    author="SBland",
    author_email="sblandcouk@gmail.com",
    description="Parameter Regression GA tool",
    long_description=long_description,
    python_requires='>=3.6',
    setup_requires=[
        'pytest-cov',
        'pytest-runner',
        'snapshottest'
    ],
    tests_require=['pytest', 'numpy'],
    extras_require={'test': ['pytest', 'numpy']},
    install_requires=['numpy'],
    packages=setuptools.find_packages(),
    package_dir={'paramga': 'paramga'},
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        'License :: OSI Approved :: MIT License',
    ],
    keywords='genetic algorithm, optimization, scientific modelling',  # Optional
)
