from setuptools import setup, find_packages
import pathlib
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')
setup(
    name='mdtex2html',
    version='0.9.1',
    description='library to convert Markdown with included LaTeX-Formulas to HTML with MathML',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/polarwinkel/mdtex2html',
    author='Dirk Winkel',
    author_email='it@polarwinkel.de',
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Topic :: Text Processing :: Markup',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Text Processing :: Markup :: LaTeX',
        'Topic :: Text Processing :: Markup :: Markdown',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='TeX, LaTeX, Markdown, HTML markdown2html, latex2mathml',
    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    packages=find_packages(),
    python_requires='>=3.6, <4',
    install_requires=['markdown', 'latex2mathml'],
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/polarwinkel/mdtex2html/issues',
        'Source': 'https://github.com/polarwinkel/mdtex2html',
    },
)
