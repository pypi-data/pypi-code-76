import shutil
from os import path
import os
import json
import importlib.resources
import pkgutil


def delete_folder_tree(folder_path):
    if path.exists(folder_path):
        print("Recursively deleting dir tree @: " + folder_path)
        try:
            shutil.rmtree(folder_path)
        except:
            print("Error while deleting temp folder")
    else:
        print("No directory exists @: " + folder_path)


def delete_file(file_path):
    if path.exists(file_path):
        print("Removing file: " + str(file_path))
        try:
            os.remove(file_path)
        except:
            print("Error deleting the file: " + file_path)
    else:
        print("No such file exists: " + file_path)


def load_validation_json():
    # with open('validation_key_ans.json', 'r') as openfile:
    #     valid_key_ans_dict = json.load(openfile)
    #     return valid_key_ans_dict
    json_data = pkgutil.get_data('time_daily_report', 'validation_key_ans.json')
    return json.loads(json_data)
    # with importlib.resources.path('time_daily_report', 'validation_key_ans.json') as openfile:
    #     valid_key_ans_dict = json.load(openfile)
    #     return valid_key_ans_dict
