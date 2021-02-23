from lyncs_setuptools import setup

setup(
    "lyncs_setuptools",
    entry_points={
        "console_scripts": [
            "lyncs_packages = lyncs_setuptools.packages:print_packages",
            "lyncs_setuptools = lyncs_setuptools:print_keys",
            "lyncs_find_package = lyncs_setuptools.cmake:print_find_package",
            "lyncs_pylint = lyncs_setuptools.pylint:run_pylint [pylint]",
            "lyncs_pylint_badge = lyncs_setuptools.pylint:print_pylint_badge [pylint]",
        ]
    },
    install_requires=[
        "gitpython",
        "pip",
    ],
    data_files=[
        ("test", ["test/CMakeLists.txt"]),
    ],
    extras_require={
        "test": ["pytest", "pytest-cov"],
        "pylint": ["pylint", "pyenchant", "lyncs_utils"],
        "cmake": ["cmake"],
    },
)
