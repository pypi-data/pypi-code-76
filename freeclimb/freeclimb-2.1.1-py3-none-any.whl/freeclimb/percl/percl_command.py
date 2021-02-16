import json

def to_json(*percl_commands):
    return json.JSONEncoder().encode(percl_commands)