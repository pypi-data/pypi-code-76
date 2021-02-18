import json 

def read_json_file(path):
    with open(path, "r") as repos_json_file:
        return json.loads(repos_json_file.read())

def handle_each_in_json_array(json_object, callback):
    for x in repos_json:
        callback(x)

def is_json_file(file_name):
    return file_name.endswith(".json")
