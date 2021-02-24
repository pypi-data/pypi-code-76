import os
import sys
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
RC_FILES = os.path.join(DIR_PATH, 'rcfiles')
sys.path.append("%s/../" % os.path.dirname(__file__))
from devilparser import rcfile

def get_username(yaml_file):
    return rcfile.parse(os.path.join(RC_FILES, yaml_file))['username']

def get_password(yaml_file):
    return rcfile.parse(os.path.join(RC_FILES, yaml_file))['password']

def test_username():
    assert(get_username('shell.yaml')) == 'shell_username'

def test_password():
    assert(get_password('shell.yaml')) == 'shell_password'
