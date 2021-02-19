from setuptools import setup, find_packages

setup(
    name="flask_sentry_requests_distributed_tracing",
    version="1.1.1",
    description="Utilities",
    url="https://github.com/shuttl-tech/flask_sentry_requests_distributed_tracing",
    author="Shuttl",
    author_email="sherub.thakur@shuttl.com",
    license="MIT",
    packages=find_packages(),
    classifiers=["Programming Language :: Python :: 3.7"],
    install_requires=["requests", "sentry_sdk", "flask"],
    extras_require={
        "test": ["pytest", "pytest-runner", "pytest-cov", "pytest-pep8", "responses"],
        "dev": ["flake8"],
    },
)
