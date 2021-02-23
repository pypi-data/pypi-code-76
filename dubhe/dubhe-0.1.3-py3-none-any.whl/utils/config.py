import pathlib

VERSION = '0.1.3'
PROG = 'dubhe'
HOME = pathlib.Path.home().joinpath('.dubhe')
DB_FILE = pathlib.Path(HOME).joinpath('dubhe.db')
