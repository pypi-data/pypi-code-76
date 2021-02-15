import setuptools

with open('README.md', 'r') as rdm:
    long_description = rdm.read()

setuptools.setup(
    name='pythumbnailer',
    version='0.6.1',
    author='somini',
    author_email='dev@somini.xyz',
    description='Create static HTML galleries with thumbnails',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/somini/pythumbnailer/',
    classifiers=[
        'Environment :: Console',
        'Environment :: Web Environment',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.8',
    install_requires=[  # Dependencies
        'jinja2',
        'pillow',
        'argparse_utils',
    ],
    entry_points={
        'console_scripts': [
            'pypublish = pythumbnailer.pypublish:__main__',
            'pypublish-clean = pythumbnailer.clean:__main__',
            'pypublish-prepare = pythumbnailer.prepare:__main__',
        ],
    },
    include_package_data=True,
)
