from pathlib import Path

import setuptools

setuptools.setup(
    name='markdown_links',
    description='Special handling for Markdown links to Markdown documents',
    long_description=(Path(__file__).parent / 'README.md').read_text(),
    long_description_content_type='text/markdown',
    keywords=['markdown', 'links'],
    version='0.0.6',
    author='Binokkio',
    author_email='binokkio@b.nana.technology',
    url='https://github.com/binokkio/markdown_links',
    license='LGPLv3+',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'markdown'
    ]
)
