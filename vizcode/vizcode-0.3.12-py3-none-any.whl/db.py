from vizcode.constants import *
import pickledb
import pickle
import base64
import os

db = pickledb.load(CURRENT_DIR_PATH + 'data.db', False)

# Store a parsed file in the db.
def store_parsed_file(parsed_file, env_path):
    f_str = open(parsed_file.file_path, 'r').read()
    data = {"client": parsed_file.client, "file": f_str, "env_path": env_path}
    b = pickle.dumps(data) # bytes of data
    encoded = base64.b64encode(b)
    db.set(os.path.abspath(parsed_file.file_path), encoded.decode('ascii'))
    db.dump()
    return

# Get the data from a parsed file in the db.
def get_file_data(file_path):
    value = db.get(os.path.abspath(file_path))
    data = pickle.loads(base64.b64decode(value))
    return data

# Returns true if the db contains a file. False otherwise. 
def contains_file(file_path):
    return db.exists(os.path.abspath(file_path))