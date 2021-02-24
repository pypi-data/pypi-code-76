from distutils.core import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.txt').read_text(encoding='utf-8')

setup(
    name='secretsauce',
    version='0.1',
    packages=['secretsauce'],
    license='LICENSE',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Deliveroo',
    author_email='diego.vazqueznanini@deliveroo.co.uk',
    url='http://pypi.python.org/pypi/secretsauce/',
)

