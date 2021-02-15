from setuptools import setup, find_packages

setup(
    name="jhreflibrary",
    version="0.0.4",
    description="jh ref library",
    packages=find_packages(),
    python_requires='>=3',
    url='https://github.com/yunjh7024/jhref',
    install_requires=[
        "aiohttp == 3.7.3",
        "black == 20.8b1",
        "holidays == 0.10.4",
        "pytz == 2019.03",
        "scikit-learn == 0.23.2",
        "scipy == 1.5.2",
        "tqdm == 4.56.0",
        "pandas == 1.1.5",
        "pylint == 2.6.0",
        "requests == 2.25.1",
        "numba == 0.52.0",
        "numpy == 1.19.5",
    ],
)