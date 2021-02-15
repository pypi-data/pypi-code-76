import os.path

import numpy as np
import validators

from inforion.helper.filehandling import checkfile_exists, loadfile
from inforion.helper.util import get_credentials


def validate_db_credentials(credentials):
    #fetch credentials file data
    cred_data = get_credentials(credentials)
    if cred_data is not None:
        #verify database information
        dict_key = {"driver":"str", "servername":"str", "username":"str", "password":"str", "database":"str"}
        verify, code, data = check_information("database", dict_key, cred_data, credentials)
        if verify == False:
            return False, code, data
    else:
        return False, "FileIsEmptyError: Credentials file empty. Please make sure to have the proper information in the file."

    return True, "200", "OK"


def check_information(main_key, dict_data, cred_data, credentials, base_dir=None):
    if main_key in cred_data:
        for key, value in dict_data.items():
            if key in cred_data[main_key]:
                if value == "url" and validators.url(cred_data[main_key]["url"]) != True:
                    return False,  "InvalidURLError: ", main_key.capitalize()+" "+key+" is not valid."
                elif value == "file" and checkfile_exists(os.path.join(base_dir, cred_data[main_key]["ionfile"])) == False:
                    return False, "FileNotFoundError: ", main_key.capitalize()+" "+key+" does not exist."
            else:
                return False, "ParameterNotFoundError: ", main_key.capitalize()+" "+key+" not found in '"+credentials+"' file"
    else:
        return False, "ParameterNotFoundError: ", main_key.capitalize()+" credentials not found in '"+credentials+"' file"
    
    return True, "200", "OK"
