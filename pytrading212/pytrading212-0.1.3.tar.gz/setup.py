from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()
setup_args = dict(
    name='pytrading212',
    version='0.1.3',
    description='Unofficial Trading212 API',
    long_description_content_type="text/markdown",
    long_description=README + "\n\n" + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Francesco Ambrosini',
    author_email='frambrosini1998@gmail.com',
    keywords=['Trading212', 'Trading212API', 'Trading212api', 'api-trading212'],
    url='https://github.com/HellAmbro/Trading212API',
)

install_requires = [
    'selenium'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
