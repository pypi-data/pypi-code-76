from setuptools import setup, find_packages

setup(
    name="nxp_lite_tools",
    version="0.1.0",
    author="Larry Shen",
    author_email="larry.shen@nxp.com",
    license="MIT",
    python_requires=">=3.4",

    packages=find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
    ],

    entry_points={
        'console_scripts': [
            'nxp_lite_tools = nxp_lite_tools:main',
        ]
    },

    extras_require={
        'pp': ['nxp_pp'],
    },

    package_data={'': ['help']},
)
