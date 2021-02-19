from setuptools import setup
from setuptools import find_packages

__version__ = "0.2.0"

# More information on setting values:
# https://github.com/Sceptre/project/wiki/sceptre-resolver-template

RESOLVER_NAME = 'sceptre-eks-lb-resolver'

RESOLVER_COMMAND_NAME = 'eks_lb_uri'

RESOLVER_MODULE_NAME = 'resolver.{}'.format(RESOLVER_COMMAND_NAME)

RESOLVER_CLASS = 'EksLbUri'

RESOLVER_DESCRIPTION = "A Sceptre resolver to retrieve a kubernetes service " \
                       "load balancer URI"

RESOLVER_AUTHOR = 'Gustavo Pantuza'

RESOLVER_AUTHOR_EMAIL = 'gustavopantuza@gmail.com'

RESOLVER_URL = 'https://github.com/pantuza/{}'.format(RESOLVER_NAME)

with open("README.md") as readme_file:
    README = readme_file.read()

install_requirements = [
    "packaging==16.8",
    "sceptre>=2.4.0",
    "kubernetes>=12.0.1",
]

test_requirements = [
    "pytest>=3.2",
]

setup_requirements = [
    "pytest-runner>=3",
]

setup(
    name=RESOLVER_NAME,
    version=__version__,
    description=RESOLVER_DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    author=RESOLVER_AUTHOR,
    author_email=RESOLVER_AUTHOR_EMAIL,
    license='Apache2',
    url=RESOLVER_URL,
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    py_modules=[RESOLVER_MODULE_NAME],
    entry_points={
        'sceptre.resolvers': [
            "{}={}:{}".format(RESOLVER_COMMAND_NAME,
                              RESOLVER_MODULE_NAME, RESOLVER_CLASS)
        ]
    },
    include_package_data=True,
    zip_safe=False,
    keywords="sceptre, sceptre-resolver, AWS EKS, k8s service load balancer,"
             "k8s lb URI, Load Balancer URI, Kubernetes Load Balancer URI, "
             "k8s lb dns, k8s service dns",
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Environment :: Console",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
    ],
    test_suite="tests",
    install_requires=install_requirements,
    tests_require=test_requirements,
    setup_requires=setup_requirements,
    extras_require={
        "test": test_requirements,
    }
)
