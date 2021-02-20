#!/usr/bin/env python
import sys
import getpass
import json
import builtins
from . import servicedefs
from infinstor_mlflow_plugin.tokenfile import read_token_file, write_token_file
from requests.exceptions import HTTPError
import requests
from os.path import expanduser
from os.path import sep as separator
import datetime
import configparser
from urllib.parse import unquote
import os

def get_creds():
    if sys.stdin.isatty():
        print("Enter your InfinStor service username and password")
        username = input("Username: ")
        password = getpass.getpass("Password: ")
    else:
        username = sys.stdin.readline().rstrip()
        password = sys.stdin.readline().rstrip()
    return username, password

def login_and_update_token_file(username, password):
    postdata = dict()
    auth_parameters = dict()
    auth_parameters['USERNAME'] = username
    auth_parameters['PASSWORD'] = password
    postdata['AuthParameters'] = auth_parameters
    postdata['AuthFlow'] = "USER_PASSWORD_AUTH"
    postdata['ClientId'] = builtins.clientid

    payload = json.dumps(postdata)

    url = 'https://cognito-idp.us-east-1.amazonaws.com:443/'
    headers = {
            'Content-Type': 'application/x-amz-json-1.1',
            'X-Amz-Target' : 'AWSCognitoIdentityProviderService.InitiateAuth'
            }

    try:
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        raise
    except Exception as err:
        print(f'Other error occurred: {err}')
        raise


    authres = response.json()['AuthenticationResult']
    token = authres['IdToken']
    refresh_token = authres['RefreshToken']

    # Call cognito REST API getUser to get custom:serviceName
    url = 'https://cognito-idp.us-east-1.amazonaws.com:443/'
    body = dict()
    body['AccessToken'] = authres['AccessToken']
    body_s = json.dumps(body)
    headers = {
            'Content-Type': 'application/x-amz-json-1.1',
            'X-Amz-Target' : 'AWSCognitoIdentityProviderService.GetUser'
            }
    try:
        response = requests.post(url, data=body_s, headers=headers)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred in getUser: {http_err}')
        raise
    except Exception as err:
        print(f'Other error occurred in getUser: {err}')
        raise
    else:
        print('cognito getUser success')
        user = response.json()
        useratt = user['UserAttributes']
        for oneattr in useratt:
            if (oneattr['Name'] == 'custom:serviceName'):
                builtins.service = oneattr['Value']
                print('Found serviceName ' + builtins.service + ' in cognito user')
                break
    if (builtins.service == None):
        print('Could not determine service')
        raise Exception('login', 'Could not determine service')

    token_time = round(datetime.datetime.timestamp(datetime.datetime.utcnow()))
    tokfile = expanduser("~") + separator + '.infinstor' + separator + 'token'
    write_token_file(tokfile, token_time, token, refresh_token, builtins.clientid,\
                builtins.service)

    payload = ("ProductCode=" + builtins.prodcode)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': token
        }

    url = 'https://api.' + builtins.service + '/customerinfo'
    try:
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        raise
    except Exception as err:
        print(f'Other error occurred: {err}')
        raise

    # print('customerinfo success')
    response_json = response.json()
    infinStorAccessKeyId = unquote(response_json.get('InfinStorAccessKeyId'))
    infinStorSecretAccessKey = unquote(response_json.get('InfinStorSecretAccessKey'))
    setup_credentials(infinStorAccessKeyId, infinStorSecretAccessKey)

    return True

def setup_credentials(infinStorAccessKeyId, infinStorSecretAccessKey):
    home = expanduser("~")
    config = configparser.ConfigParser()
    newconfig = configparser.ConfigParser()
    credsfile = home + separator + ".aws" + separator + "credentials"
    if (os.path.exists(credsfile)):
        credsfile_save = home + separator + ".aws" + separator + "credentials.save"
        try:
            os.remove(credsfile_save)
        except Exception as err:
            print()
        try:
            os.rename(credsfile, credsfile_save)
        except Exception as err:
            print()
        config.read(credsfile_save)
        for section in config.sections():
            if (section != 'infinstor'):
                newconfig[section] = {}
                dct = dict(config[section])
                for key in dct:
                    newconfig[section][key] = dct[key]
    else:
        dotaws = home + "/.aws"
        if (os.path.exists(dotaws) == False):
            os.mkdir(dotaws, 0o755)
            open(credsfile, 'a').close()

    newconfig['infinstor'] = {}
    newconfig['infinstor']['aws_access_key_id'] = infinStorAccessKeyId
    newconfig['infinstor']['aws_secret_access_key'] = infinStorSecretAccessKey

    with open(credsfile, 'w') as configfile:
        newconfig.write(configfile)

def main():
    username, password = get_creds()
    return login_and_update_token_file(username, password)

if __name__ == "__main__":
    if (main()):
        exit(0)
    else:
        exit(255)
