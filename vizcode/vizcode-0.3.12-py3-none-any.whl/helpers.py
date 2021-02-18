from vizcode.constants import *
import glob
import os
import json

# Get python files from given folder path. 
def get_files(folder_path, env_path, deselect_paths):
    files = glob.glob(folder_path + '/**/*.py', recursive=True)

    if env_path:
        env_files = set(glob.glob(env_path + "/**/*.py", recursive=True))
        files  = [file for file in files if file not in env_files]
    else:
        files = [file for file in files if 'env/' not in file]
    
    if deselect_paths:
        for subpath in deselect_paths:
            if os.path.isfile(subpath):
                files = [file for file in files if file != subpath]
            else:
                curr_dir = set(glob.glob(subpath + '/**/*.py', recursive=True))
                files = [file for file in files if file not in curr_dir]
    
    return files

def get_deselect_files(deselect_paths):
    """
    get_deselect_files returns all the files that are associated
    with any of the deselected paths either by being contained 
    in a deslected folder or being explicitly defined. 
    """
    files = set()
    for subpath in deselect_paths:
        if os.path.isfile(subpath):
            files.add(subpath)
        else:
            dir = glob.glob(subpath + '/**/*.py', recursive=True)
            files.update(dir)

    return files
    

# Removes old code files from previous graph.
def remove_old_code():
    files = glob.glob(CURRENT_DIR_PATH + PUBLIC_PATH + FILE_CODE_PATH + '/**/*.txt', recursive=True)
    for file in files:
        os.remove(file)

    return

def get_file_references(folder_path, symbols):
    """
    get_file_references gets all of the valid file references 
    from client symbols. 
    """

    folder_path += "/"
    possibilities = []
    count = len(folder_path.split("/"))

    # get all available paths from root to a given folder path
    for i in range(count):
        modified_path = "/".join(folder_path.split("/")[:-1-i])
        possibilities.append(modified_path)

    files = []
    for symbol in symbols:
        if "NON-INDEXED MODULE" in symbol:
            file = symbol.split(":")[1][1:]
            file = "/".join(file.split(".")) + ".py"
            for p in possibilities:
                guess = os.path.join(p, file)
                # check if file path exists
                if os.path.exists(guess):
                    files.append(guess)
                    break

    return files

def update_credentials():
    with open(CURRENT_DIR_PATH + CREDENTIALS_PATH, 'r') as f:  
        data = json.load(f)
        data['send_notification'] = False

    return 

# Writes user credentials to a json file. 
def write_credentials():
    with open(CURRENT_DIR_PATH + CREDENTIALS_PATH, 'w') as f:  

        creds = {
            'name': input('Enter your name: '),
            'email': input('Enter your email: '),
            'send_notification': True
        }

        json.dump(creds, f, indent=4)

        return creds

# Returns true if the user's credentials are valid. False otherwise. 
def valid_credentials():

    def validate_name(name):
        return len(name) != 0
    
    def validate_email(email):
        return len(email) != 0 and '@' in email

    WARNING_MESSAGE = "\nOops something went wrong with validating your info. " + \
    "Please enter your personal info again."
    
    with open(CURRENT_DIR_PATH + CREDENTIALS_PATH, 'r') as f: 
        try:
            data = json.load(f)
            if validate_name(data['name']) and validate_email(data['email']):
                return True
            else:
                print(WARNING_MESSAGE)
        except:
            print(WARNING_MESSAGE)

    return False