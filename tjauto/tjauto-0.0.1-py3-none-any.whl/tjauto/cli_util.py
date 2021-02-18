import os

def goto_and_exec(location_path, next_cmd):
    os.system("cd "+location_path+" && "+next_cmd)

