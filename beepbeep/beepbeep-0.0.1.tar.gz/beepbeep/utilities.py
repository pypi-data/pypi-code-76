# beepbeep.utilities: utility functions
from typing import Union, Any

import os
import json

def open_json_from_local_path(
                    filename: str, 
                    filesdir_name: str = 'download',
                    content: dict = {},
                    update_file: bool = False # Allows to add content if True. By default is False
                ) -> Any: # Union[int, str, float, dict, Any]
    """
    Open a JSON string file, create the filename if not exist and update JSON file content:


    Args:   
        filename (str): Filename will be created in case it does not exist.
        filesdir_name (str) Default="download": Directory name to save files. 
        content (dict) Default=Empty dict: Content to update JSON file
        update_file (bool) Default=False: A boolean to whether update file content or not
    
    Returns:
        A JSON object with the content of the file.

        If error:
            Return Exception or error message if applicable
    """

    if not isinstance (filename, str):
        raise TypeError('Please provide a string argument filename')
    

    ABSPATH = os.path.abspath(__file__)
    BASE_DIR = os.path.dirname(ABSPATH)
    files_dir = os.path.join(BASE_DIR, filesdir_name) # e.g: BASE_DIR/download/
    file_path = os.path.join(files_dir, filename) # e.g: BASE_DIR/download/json_file_test.py
    content_to_str = json.dumps(content)

    # arg exist_ok=True: creates and rewrite files
    try:
        os.makedirs(files_dir, exist_ok=True)
        if os.path.exists(file_path):
            if update_file is True:
                with open(file_path, 'w') as f:
                    f.write(content_to_str)
            else:
                print(f'File {filename} is in read mode')
        else:
            if update_file is True:
                with open(file_path, 'w') as f:
                    f.write(content_to_str)
            else:
                with open(file_path, 'w') as f:
                    f.write(content_to_str)

    except FileExistsError as fee:
        print(f'Cannot create a file when it already exists.')
    

    # Read filename / return content
    try:
        open_file = open(file_path, 'r')
        file_contents = json.loads(open_file.read())
        
    except FileNotFoundError as fe:
        print("No such file or directory. Please provide an existing file")
        file_contents = None
        
    except Exception as e:
        print("An error has occurred")
        file_contents = None

    
    return file_contents

print(open_json_from_local_path('json_file_test.py', content={'a':1, 'b':2}, update_file=True))

