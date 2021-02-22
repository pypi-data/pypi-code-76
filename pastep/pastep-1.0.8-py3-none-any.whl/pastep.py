# NOTES: complete documentation can found on website
# https://pastep.com/api/

# Modules
import json
import requests

# Static variables
main_url = 'https://pastep.com/api/'
base_urls = {'search': 'pastes/search?', 'trending': 'pastes/trending', 'info': 'pastes/data?',
             'account_data': 'accounts/data?'}


# App
class pastep():
    def __init__(self, api_secret, url=main_url, api_urls=base_urls):
        self.api_secret = api_secret
        self.url = url
        self.api_urls = api_urls

    # properties
    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        if 'https://pastep.com/api' in url:
            self.__url = url
        else:
            return f'Not valid url'

    @property
    def api_urls(self):
        return self.__api_urls

    @api_urls.setter
    def api_urls(self, api_urls):
        if type(api_urls) is dict:
            self.__api_urls = api_urls
        else:
            self.__api_urls = base_urls

    @property
    def api_secret(self):
        return self.__api_secret
    @api_secret.setter
    def api_secret(self, api_secret):
        self.__api_secret = api_secret
    # functions
    def create_request(self, method, values={}):
        valid = False
        method_url = f'{self.api_urls[method]}api_secret={self.api_secret}&'
        if method == 'search':
            request = requests.get(
                f"{self.url}{method_url}query={values['query']}&length={values['length']}")
            valid=True
        elif method == 'trending':
            request = requests.get(f"{self.url}{method_url}")
            valid = True
        elif method == 'info':
            request = requests.get(f"{self.url}{method_url}id={values['id']}")
            valid = True
        elif method == 'account_data':
            request = requests.get(f"{self.url}{method_url}username={values['username']}")
        response = json.loads(request.text)
        response['status_code'] = request.status_code
        return response

    def search(self, query, length=10):
        response = self.create_request('search', {'query': query, 'length': length})
        return response

    def trending(self):
        return self.create_request('trending')

    def info(self, id):
        response = self.create_request('info', {'id': id})
        return response

    def user_data(self, username):
        response = self.create_request('account_data', {'username': username})
        return response
