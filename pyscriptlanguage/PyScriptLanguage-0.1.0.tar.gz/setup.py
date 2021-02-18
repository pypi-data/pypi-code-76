from setuptools import setup
setup(
    name = 'PyScriptLanguage',
    version = '0.1.0',
    packages = ['pyscript'],
    entry_points = {
        'console_scripts': [
            'pyscript = pyscript.__main__:main'
        ]
    })
