import requests


class SerpsBot():
    def __init__(self, apikey):
        headers = {
            'Authorization': 'Bearer {}'.format(apikey)
        }
        self.headers = headers
        self.apibase = 'https://api.serpsbot.com/api/v1'

    def make_request(self, params, endpoint):
        res = requests.get(f'{self.apibase}/{endpoint}', params=params, headers=self.headers)

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

    def google_results(self, **kwargs):
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
        return self.make_request(params, endpoint='google-serps/')

    def bing_results(self, **kwargs):
        q = kwargs.get('q')
        page = kwargs.get('page', 1)

        params = {
            'q': q,
            'page': page
        }
        return self.make_request(params, endpoint='bing-serps/')