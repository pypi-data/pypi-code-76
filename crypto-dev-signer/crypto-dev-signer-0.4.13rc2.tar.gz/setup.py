from setuptools import setup

f = open('README.md', 'r')
long_description = f.read()
f.close()

requirements = []
f = open('requirements.txt', 'r')
while True:
    l = f.readline()
    if l == '':
        break
    requirements.append(l.rstrip())
f.close()

test_requirements = []
f = open('test_requirements.txt', 'r')
while True:
    l = f.readline()
    if l == '':
        break
    test_requirements.append(l.rstrip())
f.close()

setup(
        name="crypto-dev-signer",
        version="0.4.13rc2",
        description="A signer and keystore daemon and library for cryptocurrency software development",
        author="Louis Holbrook",
        author_email="dev@holbrook.no",
        packages=[
            'crypto_dev_signer.eth.signer',
            'crypto_dev_signer.eth.web3ext',
            'crypto_dev_signer.eth.helper',
            'crypto_dev_signer.eth',
            'crypto_dev_signer.keystore',
            'crypto_dev_signer.runnable',
            'crypto_dev_signer.helper',
            'crypto_dev_signer',
            ],
        install_requires=requirements,
        tests_require=test_requirements,
        long_description=long_description,
        long_description_content_type='text/markdown',
        #scripts = [
        #    'scripts/crypto-dev-daemon',
        #    ],
        entry_points = {
            'console_scripts': [
                'crypto-dev-daemon=crypto_dev_signer.runnable.signer:main',
                ],
            },
        url='https://gitlab.com/nolash/crypto-dev-signer',
        )
