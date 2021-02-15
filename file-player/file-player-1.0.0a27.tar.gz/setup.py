from setuptools import setup
import os
import fileplayer.globa

long_description_str = ""
this_dir_abs_path_str = os.path.dirname(__file__)
readme_abs_path_str = os.path.join(this_dir_abs_path_str, "README.md")

try:
    with open(readme_abs_path_str, "r") as file:
        long_description_str = '\n' + file.read()
except FileNotFoundError:
    long_description_str = fileplayer.globa.SHORT_DESCRIPTION_STR


setup(
    name=fileplayer.globa.APPLICATION_NAME_STR,
    version=fileplayer.globa.VERSION_STR,
    packages=['fileplayer'],
    url=fileplayer.globa.APPLICATION_WEBSITE_STR,
    license='GPLv3',
    author='Tord Dellsén',
    author_email='tord.dellsen@gmail.com',
    description=fileplayer.globa.SHORT_DESCRIPTION_STR,
    install_requires=["PyQt5>=5.15.2"],
    include_package_data=True,
    entry_points={"console_scripts": ["file-player=fileplayer.main:main"]},
    long_description_content_type='text/markdown',
    long_description=long_description_str,
    python_requires='>=3.8.0',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: End Users/Desktop'
    ]
)
