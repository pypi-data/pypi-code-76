import os

from setuptools import find_packages, setup


def prerelease_local_scheme(version):
    """Return local scheme version unless building on master in Gitlab.

    This function returns the local scheme version number
    (e.g. 0.0.0.dev<N>+g<HASH>) unless building on Gitlab for a
    pre-release in which case it ignores the hash and produces a
    PEP440 compliant pre-release version number (e.g. 0.0.0.dev<N>).

    """

    from setuptools_scm.version import get_local_node_and_date

    if 'CI_COMMIT_REF_NAME' in os.environ and os.environ['CI_COMMIT_REF_NAME'] == 'master':
        return ''
    else:
        return get_local_node_and_date(version)


with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='diva-boiler',
    author='Kitware, Inc.',
    author_email='kitware@kitware.com',
    description='a cli for interacting with stumpf server',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(include=['boiler']),
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'attrs',
        'boto3',
        'click>=7.0',
        'GitPython',
        'packaging',
        'python-gitlab',
        'pyxdg',
        'pyyaml',
        'requests',
        'requests-toolbelt',
        'sentry-sdk',
        'tabulate',
    ],
    entry_points={'console_scripts': ['boiler=boiler:main']},
    license='Apache Software License 2.0',
    use_scm_version={
        'local_scheme': prerelease_local_scheme,
        'root': '..',
        'relative_to': __file__,
    },
    setup_requires=['setuptools_scm'],
)
