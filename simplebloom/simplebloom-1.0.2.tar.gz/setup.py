import re
from pathlib import Path
import platform

from setuptools import setup
from setuptools import find_packages
from setuptools import Extension

# don't require Cython for building
try:
    # noinspection PyPackageRequirements
    from Cython.Build import cythonize
    HAVE_CYTHON = True
except ImportError:
    def cythonize(*_, **__):
        pass
    HAVE_CYTHON = False


PLATFORM = platform.system().lower()
ROOT_DIR = Path(__file__).parent
PACKAGE_DIR = ROOT_DIR / 'simplebloom'


def remove_c_comments(*file_paths):
    """
    https://stackoverflow.com/a/241506/6862913
    """
    def replacer(match):
        s = match.group(0)
        return ' ' if s.startswith('/') else s
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    for fp in file_paths:
        with open(fp) as f:
            text = f.read()
        new_text = re.sub(pattern, replacer, text)
        if new_text != text:
            with open(fp, 'w') as f:
                f.write(new_text)


def normalize_windows_paths(*file_paths):
    for fp in file_paths:
        with open(fp) as f:
            text = f.read()
        new_text = text.replace(r'\\', '/')
        if new_text != text:
            with open(fp, 'w') as f:
                f.write(new_text)


def make_bloom_module():
    include_dirs = [PACKAGE_DIR]
    cython_files = [PACKAGE_DIR / '_cbloom.pyx']
    for cython_file in cython_files:
        if cython_file.exists():
            cythonize(str(cython_file))

    sources = [Path('simplebloom', '_cbloom.c')]
    for source in sources:
        remove_c_comments(source)
        normalize_windows_paths(source)
    # source files must be strings
    sources = [str(source) for source in sources]

    extra_link_args = []
    extra_compile_args = []
    if PLATFORM == 'linux':
        extra_link_args.extend([
            '-Wl,'  # following are linker options
            '--strip-all,'  # Remove all symbols
            '--exclude-libs,ALL,'  # Do not export symbols
            '--gc-sections'  # Remove unused sections
        ])
        extra_compile_args.extend([
            '-O3',  # gotta go fast
        ])

    return Extension(
        'simplebloom._cbloom',
        sources,
        language='C',
        include_dirs=include_dirs,
        extra_link_args=extra_link_args,
        extra_compile_args=extra_compile_args,
    )


def read(*names):
    with ROOT_DIR.joinpath(*names).open(encoding='utf8') as f:
        return f.read()


# pip's single-source version method as described here:
# https://python-packaging-user-guide.readthedocs.io/single_source_version/
def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]',
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


setup(
    name='simplebloom',
    version=find_version('simplebloom', '__init__.py'),
    author='Joachim Folz',
    author_email='joachim.folz@dfki.de',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
    ],
    description='A dumb but fast bloom filter.',
    long_description=read('README.rst'),
    long_description_content_type='text/x-rst; charset=UTF-8',
    keywords='bloom filter bloomfilter',
    packages=find_packages(
        include=['simplebloom', 'simplebloom.*'],
    ),
    ext_modules=[make_bloom_module()],
    zip_safe=False,
    project_urls={
        'Documentation': 'https://gitlab.com/jfolz/simplebloom/blob/master/README.rst',
        'Source': 'https://gitlab.com/jfolz/simplebloom',
        'Tracker': 'https://gitlab.com/jfolz/simplebloom/issues',
    },
)
