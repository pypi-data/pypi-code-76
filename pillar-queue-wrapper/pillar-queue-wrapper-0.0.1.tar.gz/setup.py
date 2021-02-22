import setuptools

with open('README.md') as readme:
    long_desc = readme.read()

setuptools.setup(
    name='pillar-queue-wrapper',
    version='0.0.1',
    author="Pillar",
    author_email='opensource@pillar.gg',
    description='Our internal queue wrapper.',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url='https://github.com/pillargg/pillar-queue-wrapper',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'boto3>=1.17.8'
    ]
)
