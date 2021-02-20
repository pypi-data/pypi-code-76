import sys
import os
import json
import requests

from sync_dl import config as cfg

from sync_dl_ytapi.helpers import browserListener,getHttpErr

from ntpath import dirname
ytapiModulePath = dirname(__file__)

    
credPath = f'{ytapiModulePath}/credentials'
scopes = ['https://www.googleapis.com/auth/youtubepartner']

authServer = "https://sync-dl.com/auth"



#checks if sync-dl auth server is live
def authServerLive():
    response = requests.get(f"{authServer}/siteup")
    return response.ok

def newCredentials():
    cfg.logger.debug("Getting New Credentials")
    if not authServerLive():
        cfg.logger.error("Auth Server Down")
        return 

    data = browserListener(f'{authServer}/')

    if data == None:
        cfg.logger.error("Authentification Time Out")
        return
    try:
        credJson = json.loads(data)
    except:
        cfg.logger.error("Failed to Get Credentials")
        return

    if os.path.exists(credPath):
        os.remove(credPath)
    with open(credPath,"w") as f:
        json.dump(credJson,f)

    cfg.logger.info("Authentification Completed!")
    return credJson


def getCredentials():
    if os.path.exists(credPath):
        try: # if credentials cannot be unencrypted, prompt login 
            with open(credPath,"r") as f:
                credJson = json.load(f)
        except:
            
            credJson = newCredentials()

        else:
            #Refresh token
            response = requests.put(f"{authServer}/refresh",data=json.dumps(credJson))

            if not response.ok:
                cfg.logger.error(getHttpErr(response))
                cfg.logger.error("Unable to Refresh Token Continuing With Old Token")
                return credJson

            content = response.content.decode("utf-8")
            if content == None: # server could not refresh access token
                credJson = newCredentials()
            else:
                credJson = json.loads(content)
                if os.path.exists(credPath):
                    os.remove(credPath)
                with open(credPath,"w") as f:
                    json.dump(credJson,f)
    else:
        credJson = newCredentials()

    return credJson


def revokeTokens():
    if os.path.exists(credPath):

        credJson = getCredentials()
        accessToken = credJson["token"]
        response = requests.post('https://oauth2.googleapis.com/revoke',
            params={'token': accessToken},
            headers = {'content-type': 'application/x-www-form-urlencoded'})

        if not response.ok:
            cfg.logger.error(getHttpErr(response))
            cfg.logger.error("Failed to Log Out")
            answer = input("Would You Like To Delete Local Credentials Anyway? (y/n): ").lower()
            if answer != "y":
                return

        os.remove(credPath)
        cfg.logger.info("Logged Out")
    else:
        cfg.logger.error("Not Logged In")