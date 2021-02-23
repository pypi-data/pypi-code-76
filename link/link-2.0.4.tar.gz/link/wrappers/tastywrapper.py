from link.common import APIResponse
from link.wrappers import APIRequestWrapper, APIResponseWrapper
from requests.auth import AuthBase
import json
import requests


class TastyAuth(AuthBase):
    """
    Does the authentication for Spring requests.  
    """
    def __init__(self, token):
        # setup any auth-related data here
        self.token = token

    def __call__(self, r):
        # modify and return the request
        r.headers['Authorization'] = self.token
        return r


class TastyAPI(APIRequestWrapper):
    """
    Wrap the Spring API
    """
    headers = { "Content-Type": "application/json" }

    def __init__(self, wrap_name=None, base_url=None, user=None, password=None):
        self._token = None
        super(TastyAPI, self).__init__(wrap_name = wrap_name, 
                                                       base_url=base_url,
                                                       user=user,
                                                       password=password,
                                                       response_wrapper = APIResponseWrapper)

    def authenticate(self):
        """
        Write a custom auth property where we grab the auth token and put it in 
        the headers
        """
        #it's weird i have to do this here, but the code makes this not simple
        auth_json={'login':self.user, 'password':self.password}
        #send a post with no auth. prevents an infinite loop
        auth_response = self.post('/sessions', data = json.dumps(auth_json), auth =
                                 None)

        _token =  auth_response.json['data']['session-token']

        self._token = _token
        self._wrapped.auth = TastyAuth(_token) 

    @property
    def token(self):
        """
        Returns the token from the api to tell us that we have been logged in
        """
        if not self._token:
            self._token = self.authenicate().token

        return self._token




