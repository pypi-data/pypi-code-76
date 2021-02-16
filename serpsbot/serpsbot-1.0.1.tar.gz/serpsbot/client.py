import requests


class SerpsBot():
    def __init__(self, apikey):
        headers = {
            'Authorization': 'Bearer {}'.format(apikey)
        }
        self.headers = headers
        self.apibase = 'https://api.serpsbot.com/api/v1/google-serps/'

    def getresults(self, **kwargs):
        q = kwargs.get('q')
        hl = kwargs.get('hl', 'en-US')
        gl = kwargs.get('gl', 'us')
        page = kwargs.get('page', 1)
        duration = kwargs.get('duration', '')
        autocorrect = kwargs.get('autocorrect', '1')

        params = {
            'q': q,
            'hl': hl,
            'gl': gl,
            'page': page,
            'duration': duration,
            'autocorrect': autocorrect
        }
        res = requests.get(self.apibase, params=params, headers=self.headers)

        if res.status_code == 200:
            return {
                'status': True,
                'data': res.json()
            }
        else:
            return {
                'status': False,
                'data': res.json()
            }