from pathlib import Path

import setuptools


def get_all_packages(abs_path: str, pcg_name: Path):
    if pcg_name.is_dir() and (pcg_name / '__init__.py').exists():
        pcg_abs_name = f"{abs_path and abs_path + '.'}{pcg_name.stem}"
        yield pcg_abs_name

        for pcg_obj in pcg_name.iterdir():
            yield from get_all_packages(pcg_abs_name, pcg_obj)


with open('README.md', 'r') as fh:
    long_description = fh.read()

with open('api_connectors/requirements.txt', 'r') as reqs:
    requirements = [r.strip() for r in reqs.readlines()]

setuptools.setup(
    name='api_connectors',
    version='3.0',
    author='Newander',
    author_email='dasparadeis@gmail.com',
    description='A small example package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Newander/api_connectors',
    packages=list(get_all_packages('', Path('api_connectors'))),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    setup_requires=requirements,
    install_requires=requirements
)
