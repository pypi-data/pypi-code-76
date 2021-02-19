import config

import json
import os

def get_profile():
    try:
        with open(os.path.join(config.PROPERTY_FOLDER, 'profile.json'), 'r') as f:
            profile = json.loads(f.read())
        return (profile['login'], profile['password'])
    except json.decoder.JSONDecodeError:
        return ('','')

def set_profile(login,password):
    data = {'login': login, 'password': password}
    profile = json.dumps(data)
    with open(os.path.join(config.PROPERTY_FOLDER, 'profile.json'), 'w') as f:
        f.write(profile)