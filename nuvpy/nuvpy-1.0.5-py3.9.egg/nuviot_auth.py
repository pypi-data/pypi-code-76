import urllib3.request
import urllib.parse
import json
import certifi

class AuthContext:
    @classmethod
    def for_user(cls, appid, uid, pwd, url="https://api.nuviot.com"):
        cls.auth_type = 'user'
        cls.appid = appid
        cls.uid = uid
        cls.pwd = pwd
        cls.url = url
        cls.auth_token = ''
        cls.auth_token_expires = ''
        cls.refresh_token = ''
        cls.refresh_expires = ''
        cls.auth_expires = ''
        cls.app_instance_id = ''
        return cls()
    
    @classmethod
    def for_client_app(cls, clientid, client_token, url="https://api.nuviot.com"):
        cls.auth_type = 'clientapp'
        cls.client_id = clientid
        cls.url = url
        cls.client_token = client_token
        return cls()
        
    def get_token(self):
        if self.auth_type == 'user':
            post = {"grantType": "password",
              "appId": self.appid,
              "deviceId": "0000000000000000000000000000",
              "appInstanceId": "0000000000000000000000000000",
              "clientType": "aiclient",
              "email": self.uid,
              "userName": self.uid,
              "password": self.pwd,
              "refreshToken": None,
              "orgId": None,
              "orgName": None
            }

            data = json.dumps(post)

            http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
            headers={'Content-Type': 'application/json'}
            client_auth_uri = "%s/api/v1/auth" % self.url
            print(client_auth_uri)
            r = http.request("POST",client_auth_uri, body=data, headers=headers, preload_content=False)

            responseJSON = ''
            for chunk in r.stream(32):
                responseJSON += chunk.decode("utf-8")

            r.release_conn()
            print("REQUESTED AUTH")
            print(responseJSON)
            ro = json.loads(responseJSON)

            self.app_instance_id = ro["result"]["appInstanceId"]
            self.auth_token_expires = ro["result"]["accessTokenExpiresUTC"]
            self.refresh_expires = ro["result"]["refreshTokenExpiresUTC"]
            self.auth_token = ro["result"]["accessToken"]
            self.refresh_token = ro["result"]["refreshToken"]
        return
