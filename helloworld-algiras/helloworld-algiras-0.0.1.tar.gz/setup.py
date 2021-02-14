from setuptools import setup

with open('./README.md', 'r') as fh:
    long_description = fh.read()

    setup(
        name='helloworld-algiras',
        version='0.0.1',
        description='Say hello',
        install_requires = [
            'blessings ~= 1.7',
        ],
        extras_required = {
            "dev": [
                "pytest>=3.7"
            ]
        },
        py_modules=['helloworld'],
        package_dir={'': 'src'},
        classifiers=[
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent'
        ],
        long_description=long_description,
        long_description_content_type='text/markdown',

        url="https://github.com/Algiras/helloworld",
        author="Algimantas Krasauskas",
        author_email="kras.algim@gmail.com"
    )