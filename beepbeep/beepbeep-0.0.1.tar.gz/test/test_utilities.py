from beepbeep.utilities import open_json_from_local_path

import os
import json



def test_open_json_from_local_path(tmpdir):
    ABS_PATH = os.path.abspath(tmpdir)
    BASE_DIR = os.path.dirname(ABS_PATH)
    filepath_name = os.path.join(tmpdir, 'json_path.py')
    initial_content = {"a": 1, "b":2}
    json.dump(initial_content, open(filepath_name, 'w')) # Initial content

    update_file = False
    update_content = {"a": 1, "b": 5}
    

    if update_file is True: 
        # Initial content should change by new update_content value. So update_content = update_content
        assert update_content == open_json_from_local_path(filepath_name, content=update_content, update_file=update_file)
    else: 
        # Initial content restart default initial_content value above. 
        # So then update_content is not equal to initial_content.
        assert initial_content == open_json_from_local_path(filepath_name, content=update_content, update_file=update_file)


    
    
    
    


    #assert json.load(open(filepath_name, 'r')) == open_json_from_local_path(filepath_name)
    
    #assert None == open_json_from_local_path('json_path.py', )

