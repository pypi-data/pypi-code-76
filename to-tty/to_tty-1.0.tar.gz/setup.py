from setuptools import setup
setup(
        name='to_tty',
        version='1.0',
        py_modules=['to_tty'],
        install_requires=['Click', 'to_tty'],
        entry_points = '''
        [console_scripts]
        to-tty=to_tty:main
        '''
)
